# UCU Reto Winter 2025 - Chatbot for Centro Ithaka

## Project description
This is the repository for the chatbot project for the Centro Ithaka, the
entrepreneurship and innovation center for the Universidad Católica del Uruguay.

The chatbot is designed to assist members of the center with various tasks,
mainly those involving the analysis of potential projects brought by students,
teachers, and other members of the university.

## Main features
- **Natural Language Processing**: The chatbot can understand and process
  natural language queries, allowing users to interact with it in a conversational
  manner.
- **Form filling**: The chatbot can fill out forms based on user input,
  streamlining the process of submitting project proposals and other documents. For
  example, it can fill out a project form with the necessary information by just
  uploading the project proposal document.
- **Deep search**: The chatbot can perform deep searches on the topics related
  to the projects, providing users with relevant information and resources. This
  can complement the form filling feature by suggesting additional information
  that may be useful for the project proposal.

## Technologies used
The project is built using Python 3.13 with [uv](https://docs.astral.sh/uv/).

The chatbot uses Vertex AI for its core functionality, which includes
natural language processing, machine learning, deep search and data analysis.
It leverages the Google Cloud Platform to access various services such as
Google Cloud Storage for file storage and Google BigQuery for data analysis.

## Docs for devs
Use [uv](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1)
as the dependency manager. On Windows you may need to restart your PC after
installation.

Avoid using `pip`, since that may make you install a dependency globally, and
other contributors won't be able to use it because of that. `uv` ensures your
builds are reproducible.

To add a dependency:

```bash
uv add name-of-dependency
```

To run the project:

```bash
uv run --env-file=.env src/main.py # Or whichever file you want.
```

You can see the expected environment variables and their structure in
[the environment parser](./src/env.py).

