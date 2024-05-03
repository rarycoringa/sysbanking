from typing import Any
from typing import Dict

from django.views.generic import View

class TemplateTitleMixin():
    template_title: str = ""
    
    def get_context_data(self: View, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
    
        context["template_title"] = self.template_title

        return context