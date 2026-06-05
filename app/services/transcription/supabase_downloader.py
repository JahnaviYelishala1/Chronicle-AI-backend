import tempfile

from app.core.supabase import supabase


def download_from_supabase(
    bucket_name: str,
    storage_path: str
) -> str:

    file_bytes = (
        supabase.storage
        .from_(bucket_name)
        .download(storage_path)
    )

    suffix = "." + storage_path.split(".")[-1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    temp_file.write(file_bytes)
    temp_file.close()

    return temp_file.name