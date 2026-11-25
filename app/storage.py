
import os
from uuid import uuid4
from pathlib import Path
from dotenv import load_dotenv
from app.config import settings
from supabase import create_client



supabase = create_client(
    supabase_url=settings().supabase_url,
    supabase_key=settings().supabase_key
)


def upload_pdf(file_path):

    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        response = supabase.storage.from_("pdf-documents").upload(
            path=file_name,
            file=f.read(),
            file_options={
                "content-type": "application/pdf",
                "upsert": "true"
            }
        )

    return response


upload_pdf("app/resume.pdf")


# supabase.storage.from_("documents").remove(
#     ["your_file_name.pdf"]
# )


