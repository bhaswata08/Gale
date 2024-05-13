<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">GALE</h1>
</p>
<p align="center">
    <em>Unleashing Insights with Precision, Creativity, and Scale.</em>
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

Gale is a sophisticated software project designed to enhance content creation and analysis through a series of automated agents. It employs an integrated approach to generate, format, summarize, and critique content, offering seamless interaction with large language models. The project streamlines the creation of structured outlines and detailed summaries, particularly for academic and open-source communities, ensuring high relevance and precision. Gales architecture, managed under strict guidelines and configured through a centralized system, is tailored to deliver consistent and high-quality outputs, positioning itself as a crucial tool for researchers and developers aiming to optimize their content development processes.

---

##  Features

|    | Feature          | Description                                                                                           |
|----|------------------|-------------------------------------------------------------------------------------------------------|
| ⚙️  | **Architecture** | Gale utilizes a modular architecture with separate agents for content extraction, summarization, and critique, linked through a graph-based workflow. |
| 🔩 | **Code Quality** | The code is structured into distinct agents with clear responsibilities, enhancing readability and maintainability. Utilizes Python extensively. |
| 📄 | **Documentation**| Extensive inline comments and dedicated YAML and TOML files for configuration. Lacks comprehensive external documentation. |
| 🔌 | **Integrations** | Integrates with external APIs and leverages the LangChain library for language model operations, supporting both local and cloud-based models. |
| 🧩 | **Modularity**   | High modularity with clear separation into agents and utilities, supporting scalable development and potential reuse in similar projects. |
| 🧪 | **Testing**      | No explicit mention of testing frameworks or tools, suggesting an area for improvement in reliability and maintainability. |
| ⚡️ | **Performance**  | The use of configurable language models and dynamic content handling suggests good performance adaptability, but no specific metrics provided. |
| 🛡️ | **Security**     | Uses environment-specific configuration for API keys and parameters, implying some level of security for operational data. |
| 📦 | **Dependencies** | Dependencies include `py`, `python-dotenv`, `ipykernel`, `langgraph`, `yaml`, `python`, `langchain-openai`, `toml`, `lock`, `langchain`, `ipywidgets`. |
| 🚀 | **Scalability**  | Designed with scalability in mind, utilizing a graph-based flow and modular agents that can independently scale based on demand. |
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

| File                                                                            | Summary                                                                                                                                                                                                                                                                                                                             |
| ---                                                                             | ---                                                                                                                                                                                                                                                                                                                                 |
| [CODEOWNERS](https://github.com/bhaswata08/gale/blob/master/CODEOWNERS)         | Assigns repository maintenance responsibilities to a specific user, @bhaswata08, ensuring accountability and streamlined management of changes and approvals within the project.                                                                                                                                                    |
| [config.yaml](https://github.com/bhaswata08/gale/blob/master/config.yaml)       | Config.yaml centralizes configuration for various components of the Gale repository, defining interaction parameters with multiple large language models, including token limits and model specifications, ensuring consistent behavior across content extraction, formatting, summarizing, and more in the softwares architecture. |
| [pyproject.toml](https://github.com/bhaswata08/gale/blob/master/pyproject.toml) | Defines the gale project’s metadata, dependencies, and development environment using Poetry, ensuring compatibility and manageability of its article generation capabilities. It specifies essential libraries and tools, aligning with the broader architecture aimed at high-quality content creation.                            |

</details>

<details closed><summary>src.agents.content_extractor</summary>

| File                                                                                                     | Summary                                                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                                      | ---                                                                                                                                                                                                                                                                                                                                                        |
| [extractor.py](https://github.com/bhaswata08/gale/blob/master/src/agents/content_extractor/extractor.py) | Empowers the content extraction process by leveraging criticism to selectively retrieve and highlight pertinent information from provided context, ensuring outputs are optimally aligned with specific critique parameters for enhanced relevance and accuracy. Utilizes configurable language models to drive precision in information extraction tasks. |

</details>

<details closed><summary>src.agents.criticizer</summary>

| File                                                                                        | Summary                                                                                                                                                                                                                                                                                                                    |
| ---                                                                                         | ---                                                                                                                                                                                                                                                                                                                        |
| [critic.py](https://github.com/bhaswata08/gale/blob/master/src/agents/criticizer/critic.py) | Critique.py operationalizes feedback mechanisms by analyzing reviews with AI-driven critiques, ensuring comprehensive evaluation based on predefined templates and configurable parameters. It integrates with external APIs, tailoring responses to enhance content review processes within the repositorys architecture. |

</details>

<details closed><summary>src.agents.format_checker</summary>

| File                                                                                                  | Summary                                                                                                                                                                                                                                                                     |
| ---                                                                                                   | ---                                                                                                                                                                                                                                                                         |
| [formatter.py](https://github.com/bhaswata08/gale/blob/master/src/agents/format_checker/formatter.py) | Format Checker ensures output from language models adheres strictly to predefined formats, enhancing consistency and reducing extraneous content by leveraging configuration settings and environment-specific parameters to dynamically select and apply formatting rules. |

</details>

<details closed><summary>src.agents.initial_summarizer</summary>

| File                                                                                                                        | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ---                                                                                                                         | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| [initial_summarizer.py](https://github.com/bhaswata08/gale/blob/master/src/agents/initial_summarizer/initial_summarizer.py) | The `initial_summarizer.py` file is a vital component of the `gale` repository, serving as the entry point for the initial summarizer agent. It generates high-quality summaries from academic papers or open-source projects, focusing on key points, significant contributions, findings, and technical approaches. The file configures a prompt template and language model, choosing between local or cloud-based models based on the configuration settings. |

</details>

<details closed><summary>src.agents.outline_generator</summary>

| File                                                                                                         | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---                                                                                                          | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| [outline_gen.py](https://github.com/bhaswata08/gale/blob/master/src/agents/outline_generator/outline_gen.py) | The `outline_gen.py` file drives the outline generator agent in the `gale` repository, creating runnables for Wikipedia page outlines. It defines classes for Wikipedia page sections, subsections, and outlines. The module imports necessary components from `langchain_openai`, `langchain_core`, and `langchain` libraries, and sets up a prompt template with a system message, a user message, and a language model (LLM) for generating outlines from given content. The module also includes feedback logic to help the agent improve its performance. |

</details>

<details closed><summary>src.graphs</summary>

| File                                                                                     | Summary                                                                                                                                                                                                                                                                          |
| ---                                                                                      | ---                                                                                                                                                                                                                                                                              |
| [gale_graph.py](https://github.com/bhaswata08/gale/blob/master/src/graphs/gale_graph.py) | Initial_summarizer, outline_gen, criticizer, extract_content, and END. The graph begins with text input, then iteratively summarizes, generates outlines, critiques, and extracts content until an ideal outline is achieved or a limit is reached, returning the final outline. |

</details>

<details closed><summary>src.utils</summary>

| File                                                                                          | Summary                                                                                                                                                                                                                                                                                                    |
| ---                                                                                           | ---                                                                                                                                                                                                                                                                                                        |
| [togetherchain.py](https://github.com/bhaswata08/gale/blob/master/src/utils/togetherchain.py) | TogetherLLM class in `togetherchain.py` integrates ChatTogetherAI with LangChain, extending the LLM framework to enhance interaction capabilities through API key management and dynamic response generation based on user inputs. This integration supports both synchronous and asynchronous operations. |

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
- [ ] `► Get rid of ai generated readme for a better readme`
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
