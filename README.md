# SUMM AI Backend Coding Challenge 👩‍💻🚀

Welcome to the SUMM AI Backend Coding Challenge! 🎉 In this challenge, you will be tasked with building a Django API that performs text translation for both HTML and plain text inputs. 🌐📝

## 🎯 Goal

Your mission, should you choose to accept it, is to create a Django API capable of translating text provided in HTML or plain text format. Your API should serve as a bridge between users and a third-party translation service.

## 🔑 Requirements

To successfully complete this challenge, make sure your Django API adheres to the following requirements:

- **Text Translation**: Your API should receive input text, translate it using a third-party API, and return the translated text to the user.

- **Content Type Specification**: Implement an attribute in your API where users can specify the content type of the input text (e.g., HTML, plain text, etc.). You can name this attribute as you prefer.

- **HTML Handling**: When the input text is in HTML format, preserve all outer tags (such as h1, h2, p, etc.), while translating only the inner text portions. This ensures that the document structure remains intact.

- **Performance**: Especially for HTML translations you should try to parallelize the translations of the texts to avoid sequential delays of single text translations.

- **User Associations**: Attach translations to specific users so that each user's translations can be tracked and retrieved.

- **Translation Retrieval**: Provide a feature in your API to fetch all translations associated with a particular user.

### 📜 Example: Translating Inner Parts

Let's illustrate the HTML handling and translation process with an example input:

```html
"<div><h2 class='editor-heading-h2' dir='ltr'><span>hallo1 as headline</span></h2><p class='editor-paragraph' dir='ltr'><br></p><p class='editor-paragraph' dir='ltr'><span>hallo2 as paragraph</span></p><p class='editor-paragraph' dir='ltr'><span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span></p></div>"
```

In this case, your API should extract the following three text portions for translation:

1. `<span>hallo1 as headline</span>`
2. `<span>hallo2 as paragraph</span>`
3. `<span>hallo3 as paragraph with </span><b><strong class='editor-text-bold'>bold</strong></b><span> inline</span>`

After translation, these segments should be reassembled into the original HTML structure, preserving the tags.

## 🌟 Ready to Begin?

You're all set to tackle the SUMM AI Backend Coding Challenge! Build a robust API that fulfills these requirements and showcases your coding skills. Happy coding! 🚀👨‍💻👩‍💻

## Submission
Please clone this repository and upload it to a new private repo.
Implement a well-organized codebase along with a README documenting the setup, key findings, and challenges.  
Add me (@flowni) to the repo for submitting it.
You have one week to complete the assignment. ⏰
