import streamlit as st
import pandas as pd
import json

# Load data from JSON file
def load_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

# Save data to JSON file
def save_data_to_json(data, json_file):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Streamlit app
def main():
    st.title('Text Detection Comparison')

    # Load data from JSON
    json_file = 'ocr_results.json'
    image_data = load_data_from_json(json_file)

    # Convert the data to a DataFrame for easier manipulation
    image_df = pd.DataFrame(image_data)

    # Display image and detected text
   
    # Filter DataFrame to show only images with no manual annotation
    image_df_filtered = image_df[image_df['text'].apply(lambda x: 'manual' not in x)]

    # Check if there are any images left to annotate
    if image_df_filtered.empty:
        st.write('All images have been annotated.')


    image_index = st.sidebar.selectbox('Select Image', image_df_filtered['image_name'])
    st.write(f"Selected Image: {image_index}")
    # Display image
    # You can display the image here if you have the image paths
    image_path = f'./selected_images/{image_index}'
    st.image(image_path, caption='Original Image', use_column_width=True)


    st.subheader('Detected Text:')
    selected_image_data = image_df_filtered[image_df_filtered['image_name'] == image_index]['text'].iloc[0]
    st.write(pd.DataFrame([selected_image_data]))  # Convert dictionary to DataFrame

    # Manual Annotation
    manual_annotation = st.checkbox('Manual Annotation')
    if manual_annotation:
        manual_text = st.text_input('Enter Manual Annotation:')
        selected_image_data['manual'] = manual_text

    # Next Image Button
    if st.button('Next Image'):
        # Save manual annotations to JSON file
        save_data_to_json(image_data, json_file)
        # Logic to move to the next image
        # You can implement logic to move to the next image here

    # Final Display
    st.subheader('Final Text:')
    st.write(pd.DataFrame([selected_image_data]))  # Convert dictionary to DataFrame

if __name__ == "__main__":
    main()
