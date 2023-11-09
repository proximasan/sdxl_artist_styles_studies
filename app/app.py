from pathlib import Path

from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import StaticFilesConfig

from app.endpoints import router
from app.utils import download_grid_file

# Static path is on ../static relative to this file
static_path = Path(__file__).parent.parent / "static"

app = Litestar(
    route_handlers=[router],
    template_config=TemplateConfig(
        directory=Path("templates").resolve(),
        engine=JinjaTemplateEngine,
    ),
    static_files_config=[StaticFilesConfig(path="/static", directories=[static_path])],
    on_startup=[download_grid_file],
)
