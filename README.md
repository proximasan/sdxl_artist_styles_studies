<a name="readme-top"></a>

# SDXL Artist Styles Studies

## Description

Offline version of [sdxl.parrotzone.art](https://sdxl.parrotzone.art/) (つ✧ω✧)つ

### Built With

Development:

* [Python 3](https://www.python.org/)
* [Poetry](https://python-poetry.org/)
* [Litestar](https://litestar.dev/)

Development Tools:

* [Pre-Commit](https://pre-commit.com/)
* [Ruff](https://docs.astral.sh/ruff/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

* On Linux/MacOs run `./start.sh`
* On Windows, run `start.bat`

## Roadmap

See the [open issues](https://github.com/axpecloud/modernapps-back-int-reservationmanager/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please clone the repo and create a pull request. Select the template that most suits your suggestion.

1. Clone the Project (`git clone https://github.com/axpecloud/modernapps-ai-api-documentation.git`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Check that you have installed pre-commit hooks with `pre-commit install`.
4. Check that your branch is up to date with `git pull origin dev` and merge if it's necessary with `git merge origin dev`.
5. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the Branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request to the `dev` branch

### Flow of Git Branching

* From Feature to Feature: squash and merge
* From Feature to Dev: squash and merge
* From Dev to Main: merge

## Run your code

To see your code in action, launch uvicorn with the following command:

```sh
litestar run -r
```

For interactive documentation, Litestar provides the following endpoints for API documentation.

* OpenAPI schema (YAML): [http://localhost:5000/schema/openapi.yml](http://localhost:5000/schema/openapi.yml)
* OpenAPI schema (JSON): [http://localhost:5000/schema/openapi.json](http://localhost:5000/schema/openapi.json)
* Redoc: [http://localhost:5000/schema/redoc](http://localhost:5000/schema/redoc)
* Swagger-UI: [http://localhost:5000/schema/swagger](http://localhost:5000/schema/swagger)
* SpotLight Elements: [http://localhost:5000/schema/elements](http://localhost:5000/schema/elements)
* RapiDoc: [http://localhost:5000/schema/rapidoc](http://localhost:5000/schema/rapidoc)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
