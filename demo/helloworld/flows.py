from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from django.utils.translation import ugettext_lazy as _

from .models import HelloWorldProcess

@frontend.register
class HelloWorldFlow(Flow):
    process_class = HelloWorldProcess
    process_title = _('Hello world')
    process_description = _('This process demonstrates hello world approval request flow.')

    lock_impl = lock.select_for_update_lock

    summary_template = _("'{{ process.text }}' message to the world")

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        with open(os.devnull, "w") as world:
            world.write(activation.process.text)
