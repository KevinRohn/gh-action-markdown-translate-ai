import os
import sys
from pathlib import Path

class InputValidator:

    @staticmethod
    def validate_input_file(file_path: str) -> None:
        """Validate that input file exists"""
        if not Path(file_path).is_file():
            raise ValueError(f"Input file does not exist: {file_path}")

    @staticmethod
    def validate_output_file(file_path: str, update_mode: bool) -> None:
        """Validate that output file path is valid"""
        if file_path is not None:
            if not update_mode and os.path.exists(file_path):
                raise ValueError(f"Output file already exists: {file_path}")
        else:
            raise ValueError("Output file path is required")     

    @staticmethod
    def validate_update_mode(update_mode: str) -> None:
        """Validate that update mode is valid"""
        if update_mode is not None:
            if update_mode.lower() not in ["true", "false"]:
                raise ValueError("Update mode must be 'true' or 'false'")

    @staticmethod
    def validate_not_empty(value: str, name: str) -> None:
        """Validate that value is not empty"""
        if not value:
            raise ValueError(f"The input {name} is required")

def main():
    try:
        service_provider = os.environ.get("INPUT_SERVICE_PROVIDER")
        model = os.environ.get("INPUT_MODEL")
        source_language = os.environ.get("INPUT_SOURCE_LANGUAGE")
        target_language = os.environ.get("INPUT_TARGET_LANGUAGE")
        input_file = os.environ.get("INPUT_FILE_PATH")
        output_file = os.environ.get("INPUT_OUTPUT_FILE_PATH")
        update_mode = os.environ.get("INPUT_UPDATE_MODE")


        print(
            "🔍 Validating inputs..."
            f"\nService provider: {service_provider}"
            f"\nModel: {model}"
            f"\nSource language: {source_language}"
            f"\nTarget language: {target_language}"
            f"\nInput file: {input_file}"
            f"\nOutput file: {output_file}"
            f"\nUpdate mode: {update_mode}"
        )

        InputValidator.validate_not_empty(service_provider, "service_provider")
        InputValidator.validate_not_empty(model, "model")
        InputValidator.validate_not_empty(source_language, "source_language")
        InputValidator.validate_not_empty(target_language, "target_language")
        InputValidator.validate_not_empty(input_file, "input_file")
        InputValidator.validate_not_empty(output_file, "output_file")
        InputValidator.validate_not_empty(update_mode, "update_mode")
        InputValidator.validate_input_file(input_file)
        InputValidator.validate_output_file(output_file, update_mode)
        InputValidator.validate_update_mode(update_mode)
  
    except ValueError as e:
        print(f"❌ Validation error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
