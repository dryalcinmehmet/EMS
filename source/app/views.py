from django.shortcuts import render, HttpResponse
from django.views import generic


def test(request):
    return HttpResponse('Hello Python World2!')


class index3Page(generic.TemplateView):
    template_name = "dash/AdminLTE/index.html"


class indexPage(generic.TemplateView):
    template_name = "dash/AdminLTE/index.html"


class starterPage(generic.TemplateView):
    template_name = "dash/AdminLTE/starter.html"


class index2Page(generic.TemplateView):
    template_name = "dash/AdminLTE/index.html"


class code_404Page(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/404.html"


class navbarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_includes/navbar.html"


class footPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_includes/foot.html"


class footerPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_includes/footer.html"


class headPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_includes/head.html"


class sidebarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_includes/sidebar.html"


class postPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_layouts/post.html"


class pagePage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_layouts/page.html"


class defaultPage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_layouts/default.html"


class homePage(generic.TemplateView):
    template_name = "dash/AdminLTE/docs/_layouts/home.html"


class raphaelTestPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/raphael/dev/raphaelTest.html"


class customloadindicatorPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/custom-load-indicator.html"


class customgridfieldPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/custom-grid-field.html"


class datamanipulationPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/data-manipulation.html"


class customviewPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/custom-view.html"


class staticdataPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/static-data.html"


class loadingbypagePage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/loading-by-page.html"


class rowsreorderingPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/rows-reordering.html"


class externalpagerPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/external-pager.html"


class validationPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/validation.html"


class batchdeletePage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/batch-delete.html"


class localizationPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/localization.html"


class sortingPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/sorting.html"


class customrowrendererPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/custom-row-renderer.html"


class basicPage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/basic.html"


class odataservicePage(generic.TemplateView):
    template_name = "dash/AdminLTE/plugins/jsgrid/demos/odata-service.html"


class galleryPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/gallery.html"


class calendarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/calendar.html"


class widgetsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/widgets.html"


class chartjsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/charts/chartjs.html"


class flotPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/charts/flot.html"


class inlinePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/charts/inline.html"


class editorsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/forms/editors.html"


class advancedPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/forms/advanced.html"


class generalPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/forms/general.html"


class fixedsidebarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/fixed-sidebar.html"


class collapsedsidebarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/collapsed-sidebar.html"


class boxedPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/boxed.html"


class fixedfooterPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/fixed-footer.html"


class topnavPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/top-nav.html"


class fixedtopnavPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/layout/fixed-topnav.html"


class project_detailPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/project_detail.html"


class e_commercePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/e_commerce.html"


class loginPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/login.html"


class projectsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/projects.html"


class blankPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/blank.html"


class code_404Page(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/404.html"


class legacyusermenuPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/legacy-user-menu.html"


class code_500Page(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/500.html"


class forgotpasswordPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/forgot-password.html"


class profilePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/profile.html"


class contactsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/contacts.html"


class invoicePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/invoice.html"


class registerPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/register.html"


class recoverpasswordPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/recover-password.html"


class project_addPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/project_add.html"


class languagemenuPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/language-menu.html"


class pacePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/pace.html"


class project_editPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/project_edit.html"


class lockscreenPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/lockscreen.html"


class invoiceprintPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/examples/invoice-print.html"


class jsgridPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/tables/jsgrid.html"


class dataPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/tables/data.html"


class simplePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/tables/simple.html"


class readmailPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/mailbox/read-mail.html"


class mailboxPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/mailbox/mailbox.html"


class composePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/mailbox/compose.html"


class ribbonsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/ribbons.html"


class buttonsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/buttons.html"


class timelinePage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/timeline.html"


class navbarPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/navbar.html"


class iconsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/icons.html"


class generalPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/general.html"


class modalsPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/modals.html"


class slidersPage(generic.TemplateView):
    template_name = "dash/AdminLTE/pages/UI/sliders.html"



