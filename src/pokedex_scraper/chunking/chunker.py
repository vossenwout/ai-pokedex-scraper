import shutil
from pathlib import Path

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from tqdm import tqdm


class MarkdownChunker:
    def __init__(
        self,
        source_dir: Path,
        save_dir: Path,
        max_input_tokens: int = 2048,
        char_per_token: int = 3,
    ) -> None:
        self.source_dir = source_dir
        self.save_dir = save_dir
        self.max_char_per_chunk = max_input_tokens * char_per_token

    def _chunk_markdown(self, md_text: str) -> list[str]:
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3"),
            ],
            strip_headers=False,
        )
        chunks = splitter.split_text(md_text)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.max_char_per_chunk,
            chunk_overlap=0,
        )
        chunks = splitter.split_documents(chunks)
        return [chunk.page_content for chunk in chunks]

    def run(self):
        md_files = list(self.source_dir.rglob("**/*.md"))
        for md_file in tqdm(md_files, desc="Chunking"):
            md_text = md_file.read_text()
            chunks = self._chunk_markdown(md_text)
            for i, chunk in enumerate(chunks):
                save_path = self.save_dir / md_file.parent.name / f"{i}.md"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                save_path.write_text(chunk)
            shutil.copy(
                md_file.parent / "metadata.json",
                self.save_dir / md_file.parent.name / "metadata.json",
            )


if __name__ == "__main__":
    chunker = MarkdownChunker(Path("data/raw"), Path("data/chunked"))
    chunker.run()
