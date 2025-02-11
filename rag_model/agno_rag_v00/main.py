from agno.agent import Agent
from agno.embedder.google import GeminiEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.google import Gemini
from agno.vectordb.pgvector import PgVector
from dotenv import load_dotenv
import os

load_dotenv()  # This loads variables from .env into the environment

# Fetch the Supabase/PostgreSQL connection URL from the environment
DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not defined in the environment. Please add it to your .env file.")

print("Using DB_URL:", DB_URL)

# Now you can access your variable like so:
google_api_key = os.getenv("GOOGLE_API_KEY")
print("Google API Key:", google_api_key)

# Create a knowledge base from a PDF URL.
# In this case, we use a PDF of Thai recipes hosted on S3.
knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    # Use PgVector to store embeddings in the "recipes" table
    vector_db=PgVector(
        table_name="documents",  # Store embeddings in the "documents" table
        db_url=DB_URL,  # Use the environment variable instead of hardcoded value
        embedder=GeminiEmbedder(),  # GeminiEmbedder handles generating embeddings
    ),
)

# Load (or recreate) the knowledge base.
# Use recreate=True on the first run to generate and store the embeddings.
knowledge_base.load(recreate=True)  # Comment out this line on subsequent runs

# Initialize the Agent using the Gemini model.
# The "id" parameter specifies the Gemini model variant you wish to use.
agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    knowledge=knowledge_base,
    show_tool_calls=True,  # If you want to see tool invocation details
)

# Use the agent to answer a question; output is formatted in markdown.
agent.print_response("How to make Thai curry?", markdown=True)
