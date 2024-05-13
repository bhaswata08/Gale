<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">GALE</h1>
</p>
<p align="center">
    <em>Unleashing Insights, Perfecting Content, Driving Innovation.</em>
</p>
<p align="center">
	<!-- Shields.io badges not used with skill icons. --><p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<a href="https://skillicons.dev">
		<img src="https://skillicons.dev/icons?i=md,py">
	</a></p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

The Gale software project serves as a comprehensive suite designed to enhance document processing and analysis. It features a series of specialized agents for content extraction, critique, formatting, summarization, and outline generation, all orchestrated through a robust graph-based state machine. Each component, from the initial summarizer that distills key document insights to the criticizer that provides detailed feedback, leverages advanced language models and configurable settings to refine output quality. Gales architecture, spearheaded by its clear ownership and modular design, significantly streamlines the handling of complex text data, making it an invaluable tool for organizations aiming to optimize their content analysis processes.

---

##  Features

|    | Feature            | Description                                                                                   |
|----|--------------------|-----------------------------------------------------------------------------------------------|
| ⚙️  | **Architecture**   | Utilizes a modular architecture with components like extractors, critics, and summarizers.   |
| 🔩 | **Code Quality**   | High code quality with clear modular division and use of Python's Poetry for dependency management. |
| 📄 | **Documentation**  | Comprehensive documentation within code; extensive inline comments in critical modules.       |
| 🔌 | **Integrations**   | Integrates with OpenAI's Chat models, LangChain, and LangGraph libraries for enhanced functionality. |
| 🧩 | **Modularity**     | Highly modular, component-based structure allows for easy extension and maintenance.          |
| 🧪 | **Testing**        | No explicit mention of testing frameworks or tools from the provided details.                |
| ⚡️  | **Performance**    | Designed for efficient data handling and processing with optimized AI model interaction.      |
| 🛡️ | **Security**       | No specific security measures detailed, but uses .env for environment variable management.    |
| 📦 | **Dependencies**   | Dependencies include Python, LangChain, LangGraph, ipywidgets, pyproject.toml, and others.   |
| 🚀 | **Scalability**    | Scalable architecture through asynchronous handling and modular design to manage increased load. |
```

---

##  Repository Structure

```sh
└── gale/
    ├── CODEOWNERS
    ├── LICENSE
    ├── Readme.md
    ├── config.yaml
    ├── poetry.lock
    ├── pyproject.toml
    ├── src
    │   ├── agents
    │   │   ├── content_extractor
    │   │   │   └── extractor.py
    │   │   ├── criticizer
    │   │   │   └── critic.py
    │   │   ├── format_checker
    │   │   │   └── formatter.py
    │   │   ├── initial_summarizer
    │   │   │   └── initial_summarizer.py
    │   │   └── outline_generator
    │   │       └── outline_gen.py
    │   ├── graphs
    │   │   └── gale_graph.py
    │   └── utils
    │       └── togetherchain.py
    └── tests
        └── test1.py
```

---

##  Modules

<details closed><summary>.</summary>

| File                                                                            | Summary                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                             | ---                                                                                                                                                                                                                                                                                                                                              |
| [CODEOWNERS](https://github.com/bhaswata08/gale/blob/master/CODEOWNERS)         | The CODEOWNERS file designates responsibility for maintaining different parts of the gale repository. Here, @bhaswata08 assumes ownership of the entire codebase. This ensures clear accountability and maintenance efficiency.                                                                                                                  |
| [config.yaml](https://github.com/bhaswata08/gale/blob/master/config.yaml)       | The `config.yaml` file in the gale repository sets essential parameters for various modules. It defines configurations for critic, format checker, formatter, initial summarizer, outline generator, and retriever components, specifying their language models and token limits. The file also configures graph settings, like iteration count. |
| [pyproject.toml](https://github.com/bhaswata08/gale/blob/master/pyproject.toml) | The `pyproject.toml` file is the configuration center for Pythons Poetry package manager in the gale' repository. It specifies project details, dependency versions, and build settings. This includes the main gale package, third-party libraries, and development tools, enhancing code modularity and reusability.                           |

</details>

<details closed><summary>src.agents.content_extractor</summary>

| File                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                                                      |
| ---                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                                                          |
| [extractor.py](https://github.com/bhaswata08/gale/blob/master/src/agents/content_extractor/extractor.py) | The `extractor.py` file orchestrates a content extractor agent that analyzes given input contexts with accompanying criticisms. It employs a retriever model to extract the most relevant information from the input context, utilizing a powerful language model and a well-crafted prompt. The output is a list of the most pertinent content, along with a rationale for each extraction. |

</details>

<details closed><summary>src.agents.criticizer</summary>

| File                                                                                        | Summary                                                                                                                                                                                                                                                                                                                                                 |
| ---                                                                                         | ---                                                                                                                                                                                                                                                                                                                                                     |
| [critic.py](https://github.com/bhaswata08/gale/blob/master/src/agents/criticizer/critic.py) | In the `gale` repository, `critic.py` critiques given reviews and corresponding sections, offering detailed analysis and feedback. It utilizes OpenAIs chat model, langchain libraries, and a custom critique model. A configurable format instructs the critique output. The critique model can be driven by either a TogetherLLM or ChatOpenAI model. |

</details>

<details closed><summary>src.agents.format_checker</summary>

| File                                                                                                  | Summary                                                                                                                                                                                                                                                                                                                                                  |
| ---                                                                                                   | ---                                                                                                                                                                                                                                                                                                                                                      |
| [formatter.py](https://github.com/bhaswata08/gale/blob/master/src/agents/format_checker/formatter.py) | Format Checker formalizes information from a language model by adhering to specified formats, ensuring completeness, eliminating unnecessary data, and maintaining adherence to instructions. It achieves this through a system prompt, ChatPromptTemplate, and Langchains LLM. The output is a well-structured, concise response in the desired format. |

</details>

<details closed><summary>src.agents.initial_summarizer</summary>

| File                                                                                                                        | Summary                                                                                                                                                                                                                                                                                                                                                                |
| ---                                                                                                                         | ---                                                                                                                                                                                                                                                                                                                                                                    |
| [initial_summarizer.py](https://github.com/bhaswata08/gale/blob/master/src/agents/initial_summarizer/initial_summarizer.py) | The `initial_summarizer.py` file is the entry point for the initial summarizer agent in the `gale` repository. It generates a high-level summary of given documents, focusing on key points, significant contributions, and the technical approach. The code configures a language model to read the document, understand its contents, and output a thorough summary. |

</details>

<details closed><summary>src.agents.outline_generator</summary>

| File                                                                                                         | Summary                         |
| ---                                                                                                          | ---                             |
| [outline_gen.py](https://github.com/bhaswata08/gale/blob/master/src/agents/outline_generator/outline_gen.py) | <code>► INSERT-TEXT-HERE</code> |

</details>

<details closed><summary>src.graphs</summary>

| File                                                                                     | Summary                                                                                                                                                                                                                                                                                                          |
| ---                                                                                      | ---                                                                                                                                                                                                                                                                                                              |
| [gale_graph.py](https://github.com/bhaswata08/gale/blob/master/src/graphs/gale_graph.py) | The gale_graph.py file constructs a state machine for the GALE agent using the langgraph library. It defines a series of connected nodes, each representing an agent. The agents process text in a loop, iteratively refining an outline until it meets specified criteria or reaches a maximum iteration count. |

</details>

<details closed><summary>src.utils</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                     |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                         |
| [togetherchain.py](https://github.com/bhaswata08/gale/blob/master/src/utils/togetherchain.py) | TogetherLLM integrates ChatTogetherAI with LangChain, extending the LLM class to enable prompt-based text generation. It manages API interactions, customizes responses with configurable parameters like model choice, temperature, and token limits, and handles both synchronous and asynchronous calls. |

</details>

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the gale repository:
>
> ```console
> $ git clone https://github.com/bhaswata08/gale
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd gale
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

<h4>From <code>source</code></h4>

> Run gale using the command below:
> ```console
> $ python main.py
> ```

###  Tests

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Project Roadmap

- [X] `► Initial working prototype`

- [ ] `►Add support for multiple LLMs.`
- [ ] `►Add frontend and main.py script.`
- [ ] `►Add batching for each section of document.`
- [ ] `►Add PDF support.`
- [ ] `►Add diagram support.`
- [ ] `►Add auto generation of a report(Markdown/pdf).`

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/bhaswata08/gale/issues)**: Submit bugs found or log feature requests for the `gale` project.
- **[Submit Pull Requests](https://github.com/bhaswata08/gale/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/bhaswata08/gale/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/bhaswata08/gale
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com{/bhaswata08/gale/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=bhaswata08/gale">
   </a>
</p>
</details>

---

##  License

This project is protected under the [GNU Affero General Public License v3.0](https://choosealicense.com/licenses/agpl-3.0/) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/agpl-3.0/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
