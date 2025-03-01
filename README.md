# :book: GitHub Action Markdown Translate AI

> A GitHub Action to translate markdown files using custom AI models from multiple providers, including OpenAI, Anthropic, Gemini, and DeepSeek.

## :question: Why use this GitHub Action?

Translating documentation and markdown content for international audiences is essential for global projects. Manual translation is time-consuming and often inconsistent. This GitHub Action automates the translation process using state-of-the-art AI models, preserving markdown formatting and providing accurate translations with detailed usage statistics.

## About

This action allows you to automatically translate markdown files from one language to another using various AI service providers. It supports multiple AI models from different providers, tracks token usage, and preserves the original markdown structure in the translated output. The action is perfect for maintaining multilingual documentation.

## How It Works

The action uses the [markdown-translate-ai](https://github.com/KevinRohn/markdown-translate-ai) Python package to:

1. Parse the source markdown file while preserving its structure
2. Send the content to the selected AI service for translation
3. Reconstruct the markdown file in the target language
4. Generate translation statistics for monitoring and cost tracking

## Usage

>:white_flag: See the [inputs](#inputs) section for detailed descriptions.

```yaml
- name: Translate Markdown Documentation
  id: translate
  uses: KevinRohn/gh-action-markdown-translate-ai@v1
  with:
    api_key: ${{ secrets.AI_API_KEY }}
    service_provider: 'openai'
    model: 'gpt-4o'
    source_language: 'English'
    target_language: 'German'
    file_path: './docs/README.md'
    output_file_path: './docs/README.de.md'
```

## Available models

[List of available models](https://github.com/KevinRohn/markdown-translate-ai?tab=readme-ov-file#available-models) from the [markdown-translate-ai](https://github.com/KevinRohn/markdown-translate-ai) Python package.

## Example usage multiple translations using a matrix

You can aslo check the [.github/workflows/test.yml](.github/workflows/test.yml) file to see a full example.

<details>
<summary> Multiple translations </summary>

```yaml
test-translation:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        model:
          - gpt-4o
          - gpt-4o-mini
          - gpt-3.5-turbo
          - gpt-4
          - gpt-4-turbo
          - claude-3.7-sonnet-latest
          - claude-3.5-sonnet
          - claude-3.5-haiku
          - gemini-1.5-flash
        include:
          - model: gpt-4o
            service-provider: openai
            target-language: 'German'
          - model: gpt-4o-mini
            service-provider: openai
            target-language: 'Italian'
          - model: gpt-3.5-turbo
            service-provider: openai
            target-language: 'French'
          - model: gpt-4
            service-provider: openai
            target-language: 'Spanish'
          - model: gpt-4-turbo
            service-provider: openai
            target-language: 'Portuguese'
          - model: claude-3.7-sonnet-latest
            service-provider: anthropic
            target-language: 'German'
          - model: claude-3.5-sonnet
            service-provider: anthropic
            target-language: 'German'
          - model: claude-3.5-haiku
            service-provider: anthropic
            target-language: 'Italian'
          - model: gemini-1.5-flash
            service-provider: gemini
            target-language: 'German'

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Test translation file
        id: file_info
        run: |
          echo "source_file=test/en/example.md" >> $GITHUB_OUTPUT
          echo "target_file=example.md" >> $GITHUB_OUTPUT

      - name: Select API Key based on Service provider
        run: | # shell
          case ${{ matrix.service-provider }} in
            openai)
              echo "API_KEY=${{ secrets.OPENAI_API_KEY }}" >> $GITHUB_ENV
              ;;
            anthropic)
              echo "API_KEY=${{ secrets.ANTHROPIC_API_KEY }}" >> $GITHUB_ENV
              ;;
            gemini)
              echo "API_KEY=${{ secrets.GEMINI_API_KEY }}" >> $GITHUB_ENV
              ;;
            deepseek)
              echo "API_KEY=${{ secrets.DEEPSEEK_API_KEY }}" >> $GITHUB_ENV
              ;;
          esac

      - name: Translate using ${{ matrix.model }} (${{ matrix.service-provider }})
        id: translation
        uses: ./
        with:
          api_key: ${{ env.API_KEY }}
          service_provider: ${{ matrix.service-provider }}
          model: ${{ matrix.model }}
          source_language: English
          target_language: ${{ matrix.target-language }}
          file_path: ${{ steps.file_info.outputs.source_file }}
          output_file_path: ${{ steps.file_info.outputs.target_file }}

      - name: Show Summary output
        shell: bash
        run: | # shell
          echo "## Translation summary for ${{ matrix.model }} (${{ matrix.service-provider }})" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "| Metric | Value |" >> $GITHUB_STEP_SUMMARY
          echo "|--------|-------|" >> $GITHUB_STEP_SUMMARY
          echo "| Total tokens | **${{ steps.translation.outputs.total_tokens_used }}** |" >> $GITHUB_STEP_SUMMARY
          echo "| Input tokens | **${{ steps.translation.outputs.input_tokens_used }}** |" >> $GITHUB_STEP_SUMMARY
          echo "| Output tokens | **${{ steps.translation.outputs.output_tokens_used }}** |" >> $GITHUB_STEP_SUMMARY
          echo "| Duration | **${{ steps.translation.outputs.duration_seconds }}** seconds |" >> $GITHUB_STEP_SUMMARY
          
          # Display source and translated content in step summary
          echo "<details><summary>Source content</summary>" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          cat ${{ steps.file_info.outputs.source_file }} >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "</details>" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY

          echo "<details><summary>Translated content in ${{ matrix.target-language }}</summary>" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          cat ${{ steps.file_info.outputs.target_file }} >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "</details>" >> $GITHUB_STEP_SUMMARY
```

</details>


## Inputs

The action supports the following inputs:

- `api_key`  
  API key for the translation service provider.  
  Required: true

- `service_provider`  
  Translation AI service provider to use.  
  Options: openai, anthropic, gemini, deepseek  
  Required: true  
  Default: 'openai'

- `model`  
  Model to use for translation.  
  Required: true  
  Default: 'gpt-4o'

- `source_language`  
  Source language of the markdown file.  
  Required: true  
  Default: 'English'

- `target_language`  
  Target language for the translation.  
  Required: true  
  Default: 'German'

- `file_path`  
  Path to the source markdown file to be translated.  
  Required: true

- `output_file_path`  
  Path where the translated markdown file will be saved.  
  Required: true

- `update_mode` - **EXPERIMENTAL - In Progress**
  If set to true, the original markdown file will be updated with the translated content.  
  Required: false  
  Default: false

## Outputs

- `total_tokens_used`  
  Total number of tokens used for the translation operation.

- `input_tokens_used`  
  Number of input tokens processed during translation.

- `output_tokens_used`  
  Number of output tokens generated during translation.

- `duration_seconds`  
  Duration of the translation process in seconds.