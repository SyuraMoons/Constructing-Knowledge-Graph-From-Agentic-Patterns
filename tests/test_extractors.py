"""
Simple Tests for Extractors
"""
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "extractors"))

from crewai_extractor import CrewAIExtractor
from langraph_extractor import LangGraphExtractor
from autogen_extractor import AutoGenExtractor
from mastraai_extractor import MastraAIExtractor


def test_crewai_extractor():
    """Test CrewAI extractor"""
    print("Testing CrewAI extractor...")

    extractor = CrewAIExtractor()
    test_file = Path("../data/raw/crewai/example1.py")

    if test_file.exists():
        result = extractor.process_file(test_file)
        assert result is not None, "Extraction failed"
        assert "agents" in result, "No agents extracted"
        assert result["framework"] == "crewai"
        print(f"  ✅ Extracted {len(result['agents'])} agents, {len(result['tasks'])} tasks")
    else:
        print(f"  ⚠️  Test file not found: {test_file}")


def test_output_format():
    """Test that output has required fields"""
    print("Testing output format...")

    extractor = CrewAIExtractor()
    test_file = Path("../data/raw/crewai/example1.py")

    if test_file.exists():
        result = extractor.process_file(test_file)

        required_fields = ["id", "framework", "agents", "tasks", "provenance"]
        for field in required_fields:
            assert field in result, f"Missing required field: {field}"

        print("  ✅ All required fields present")
    else:
        print(f"  ⚠️  Test file not found: {test_file}")


def test_json_serializable():
    """Test that output is JSON serializable"""
    print("Testing JSON serialization...")

    extractor = CrewAIExtractor()
    test_file = Path("../data/raw/crewai/example1.py")

    if test_file.exists():
        result = extractor.process_file(test_file)

        try:
            json_str = json.dumps(result, indent=2)
            assert len(json_str) > 0
            print("  ✅ Output is valid JSON")
        except Exception as e:
            print(f"  ❌ JSON serialization failed: {e}")
            raise
    else:
        print(f"  ⚠️  Test file not found: {test_file}")


def run_all_tests():
    """Run all tests"""
    print("\n🧪 Running Extractor Tests\n")
    print("="*50)

    tests = [
        test_crewai_extractor,
        test_output_format,
        test_json_serializable
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ❌ Test failed: {e}")

    print("="*50)
    print(f"\n📊 Results: {passed} passed, {failed} failed\n")


if __name__ == "__main__":
    run_all_tests()
