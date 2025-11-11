"""
Simple Main Pipeline for Agentic Pattern Extraction
Processes all framework files and generates normalized JSON output
"""
import json
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import crewai_extractor
import langraph_extractor
import autogen_extractor
import mastraai_extractor


# Directories
DATA_RAW = Path("../../data/raw")
DATA_NORMALIZED = Path("../../data/normalized")
DATA_NORMALIZED.mkdir(parents=True, exist_ok=True)


def process_all():
    """Process all frameworks"""

    extractors = {
        "crewai": crewai_extractor.CrewAIExtractor(),
        "langraph": langraph_extractor.LangGraphExtractor(),
        "autogen": autogen_extractor.AutoGenExtractor(),
        "mastraai": mastraai_extractor.MastraAIExtractor()
    }

    stats = {"total": 0, "success": 0, "failed": 0}

    for framework_name, extractor in extractors.items():
        framework_dir = DATA_RAW / framework_name

        if not framework_dir.exists():
            print(f"WARNING: Directory not found: {framework_dir}")
            continue

        print(f"\n[Processing {framework_name}...]")

        # Process all files in framework directory
        for file_path in framework_dir.rglob("*"):
            if file_path.suffix in ['.py', '.json', '.yaml', '.yml']:
                stats["total"] += 1

                try:
                    # Extract and normalize
                    normalized = extractor.process_file(file_path)

                    if normalized:
                        # Save to normalized directory
                        output_file = DATA_NORMALIZED / f"{normalized['id']}.json"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(normalized, f, indent=2, ensure_ascii=False)

                        stats["success"] += 1
                        print(f"  OK {file_path.name} -> {normalized['id']}.json")
                    else:
                        stats["failed"] += 1
                        print(f"  FAIL {file_path.name} (extraction failed)")

                except Exception as e:
                    stats["failed"] += 1
                    print(f"  FAIL {file_path.name}: {e}")

    # Print summary
    print(f"\n{'='*60}")
    print(f"EXTRACTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total files processed: {stats['total']}")
    print(f"Successfully extracted: {stats['success']}")
    print(f"Failed: {stats['failed']}")
    print(f"Output directory: {DATA_NORMALIZED.absolute()}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print(">> Starting Agentic Pattern Extraction...\n")
    process_all()
    print("\n>> Done!")
