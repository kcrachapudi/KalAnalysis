import streamlit as st

def Custom_TextInput(label, default_value, key):
    """
    Create a custom text input field with a default value.

    Args:
        label (str): The label for the text input field.
        default_value (str): The default value for the text input field.
        key (str): The key for the text input field.

    Returns:
        None
    """
    # Create a text input field with the specified label, default value, and key
    st.text_input(label, value=default_value, key=key)
    

def Custom_TextArea(label, default_value, key):
    """
    Create a custom text area with a default value.

    Args:
        label (str): The label for the text area.
        default_value (str): The default value for the text area.
        key (str): The key for the text area.

    Returns:
        None
    """
    # Create a text area with the specified label, default value, and key
    st.text_area(label, value=default_value, key=key)
    
    
def Custom_SelectBox(label, options, key):
    """
    Create a custom select box with a list of options.

    Args:
        label (str): The label for the select box.
        options (list): A list of options for the select box.
        key (str): The key for the select box.

    Returns:
        None
    """
    # Create a select box with the specified label, options, and key
    st.selectbox(label, options, key=key)
    
    
def Custom_Button(label, key, action):
    """
    Create a custom button with a label.

    Args:
        label (str): The label for the button.
        key (str): The key for the button.
        action (function): The function to be executed when the button is clicked.
    Returns:
        None
    """
    # Create a button with the specified label and key
    st.button(label=label, key=key, on_click=action)