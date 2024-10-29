import base64
import time

import streamlit as st

from ai_operations import compare_documents, get_claude_and_llama_models
from config import MAX_FILE_SIZE
from file_operations import delete_file, save_file


def is_claude_model(model_id):
    return model_id.startswith("anthropic.")


def get_default_max_tokens(model_id):
    return 4096 if is_claude_model(model_id) else 2048


def display_pdf(file):
    base64_pdf = base64.b64encode(file.getvalue()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    st.set_page_config(layout="wide")
    st.title("Document Comparison using Amazon Bedrock")

    # Generate a unique key for this session
    if "session_id" not in st.session_state:
        st.session_state.session_id = int(time.time() * 1000)

    col1, col2 = st.columns(2)

    with col1:
        # Get Claude and Llama models
        model_options = get_claude_and_llama_models()

        # Set default model
        default_model = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        if default_model not in model_options:
            default_model = model_options[0]

        # Model selection dropdown with default option
        selected_model = st.selectbox(
            "Select Bedrock Model",
            model_options,
            index=model_options.index(default_model),
        )

        # Max tokens slider
        default_max_tokens = get_default_max_tokens(selected_model)
        max_tokens = st.slider(
            "Max Tokens",
            min_value=1,
            max_value=4096,
            value=default_max_tokens,
            step=1,
            help="Maximum number of tokens for the model output.",
        )

    with col2:
        # Calculate max file size in MB for display
        max_size_mb = MAX_FILE_SIZE / (1024 * 1024)

        # File uploaders with unique keys and custom help text
        pdf_file1 = st.file_uploader(
            "Choose first PDF file",
            type="pdf",
            key=f"uploader1_{st.session_state.session_id}",
            help=f"Maximum file size: {max_size_mb:.2f} MB",
        )
        pdf_file2 = st.file_uploader(
            "Choose second PDF file",
            type="pdf",
            key=f"uploader2_{st.session_state.session_id}",
            help=f"Maximum file size: {max_size_mb:.2f} MB",
        )

        # Buttons side by side with custom styles
        button_col1, button_col2 = st.columns(2)
        with button_col1:
            compare_button = st.button(
                "Compare Documents", key="compare", use_container_width=True
            )
        with button_col2:
            reset_button = st.button("Reset App", key="reset", use_container_width=True)

    if reset_button:
        st.session_state.session_id = int(time.time() * 1000)
        st.rerun()

    # PDF Previews and Comparison Results
    st.subheader("PDF Previews and Comparison Results")
    preview_col, result_col = st.columns(2)

    with preview_col:
        st.subheader("PDF Previews")
        if pdf_file1:
            st.write("PDF 1 Preview")
            display_pdf(pdf_file1)

        if pdf_file2:
            st.write("PDF 2 Preview")
            display_pdf(pdf_file2)

    with result_col:
        st.subheader("Comparison Result")

        # Check file sizes and process
        if pdf_file1 and pdf_file2:
            if pdf_file1.size > MAX_FILE_SIZE or pdf_file2.size > MAX_FILE_SIZE:
                st.error(
                    f"One or both files exceed the maximum size of {max_size_mb:.2f} MB. Please upload smaller files."
                )
            elif compare_button:
                file_path1 = None
                file_path2 = None
                try:
                    # Save files
                    file_path1 = save_file(pdf_file1)
                    file_path2 = save_file(pdf_file2)

                    if file_path1 and file_path2:
                        # Compare documents using the selected model and max tokens
                        comparison_result = compare_documents(
                            file_path1, file_path2, selected_model, max_tokens
                        )

                        # Display comparison result
                        st.write(comparison_result)
                    else:
                        st.error("Error saving files. Please try again.")

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.error(
                        "The comparison failed. This may be due to model limitations, incompatibility, or an issue with the input documents. Please try a different model or check your input files."
                    )

                finally:
                    # Clean up: delete saved files
                    if file_path1:
                        delete_file(file_path1)
                    if file_path2:
                        delete_file(file_path2)


if __name__ == "__main__":
    main()
