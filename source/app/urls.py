from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from . import views

# Personalized admin site settings like title and header
admin.site.site_title = "Battery Site Admin"
admin.site.site_header = "Battery Administration"

# User-uploaded files like profile pics need to be served in development

urlpatterns= [


    path("", views.test, name="test"),
    path("starter/", views.starterPage.as_view(), name="starter"),
    path("index/", views.indexPage.as_view(), name="index"),
    path("index2/", views.index2Page.as_view(), name="index2"),
    path("index3/", views.index3Page.as_view(), name="index3"),
    path("code_404", views.code_404Page.as_view(), name="code_404"),
    path("navbar/", views.navbarPage.as_view(), name="navbar"),
    path("foot/", views.footPage.as_view(), name="foot"),
    path("footer/", views.footerPage.as_view(), name="footer"),
    path("head/", views.headPage.as_view(), name="head"),
    path("sidebar/", views.sidebarPage.as_view(), name="sidebar"),
    path("post/", views.postPage.as_view(), name="post"),
    path("page/", views.pagePage.as_view(), name="page"),
    path("default/", views.defaultPage.as_view(), name="default"),
    path("home/", views.homePage.as_view(), name="home"),
    path("raphaelTest/", views.raphaelTestPage.as_view(), name="raphaelTest"),
    path("customloadindicator/", views.customloadindicatorPage.as_view(), name="customloadindicator"),
    path("customgridfield/", views.customgridfieldPage.as_view(), name="customgridfield"),
    path("datamanipulation/", views.datamanipulationPage.as_view(), name="datamanipulation"),
    path("customview/", views.customviewPage.as_view(), name="customview"),
    path("staticdata/", views.staticdataPage.as_view(), name="staticdata"),
    path("loadingbypage/", views.loadingbypagePage.as_view(), name="loadingbypage"),
    path("rowsreordering/", views.rowsreorderingPage.as_view(), name="rowsreordering"),
    path("externalpager/", views.externalpagerPage.as_view(), name="externalpager"),
    path("validation/", views.validationPage.as_view(), name="validation"),
    path("batchdelete/", views.batchdeletePage.as_view(), name="batchdelete"),
    path("localization/", views.localizationPage.as_view(), name="localization"),
    path("sorting/", views.sortingPage.as_view(), name="sorting"),
    path("customrowrenderer/", views.customrowrendererPage.as_view(), name="customrowrenderer"),
    path("basic/", views.basicPage.as_view(), name="basic"),
    path("odataservice/", views.odataservicePage.as_view(), name="odataservice"),
    path("gallery/", views.galleryPage.as_view(), name="gallery"),
    path("calendar/", views.calendarPage.as_view(), name="calendar"),
    path("widgets/", views.widgetsPage.as_view(), name="widgets"),
    path("chartjs/", views.chartjsPage.as_view(), name="chartjs"),
    path("flot/", views.flotPage.as_view(), name="flot"),
    path("inline/", views.inlinePage.as_view(), name="inline"),
    path("editors/", views.editorsPage.as_view(), name="editors"),
    path("advanced/", views.advancedPage.as_view(), name="advanced"),
    path("general/", views.generalPage.as_view(), name="general"),
    path("fixedsidebar/", views.fixedsidebarPage.as_view(), name="fixedsidebar"),
    path("collapsedsidebar/", views.collapsedsidebarPage.as_view(), name="collapsedsidebar"),
    path("boxed/", views.boxedPage.as_view(), name="boxed"),
    path("fixedfooter/", views.fixedfooterPage.as_view(), name="fixedfooter"),
    path("topnav/", views.topnavPage.as_view(), name="topnav"),
    path("fixedtopnav/", views.fixedtopnavPage.as_view(), name="fixedtopnav"),
    path("project_detail/", views.project_detailPage.as_view(), name="project_detail"),
    path("e_commerce/", views.e_commercePage.as_view(), name="e_commerce"),
    path("login/", views.loginPage.as_view(), name="login"),
    path("projects/", views.projectsPage.as_view(), name="projects"),
    path("blank/", views.blankPage.as_view(), name="blank"),
    path("code_404", views.code_404Page.as_view(), name="code_404"),
    path("legacyusermenu/", views.legacyusermenuPage.as_view(), name="legacyusermenu"),
    path("code_500", views.code_500Page.as_view(), name="code_500"),
    path("forgotpassword/", views.forgotpasswordPage.as_view(), name="forgotpassword"),
    path("profile/", views.profilePage.as_view(), name="profile"),
    path("contacts/", views.contactsPage.as_view(), name="contacts"),
    path("invoice/", views.invoicePage.as_view(), name="invoice"),
    path("register/", views.registerPage.as_view(), name="register"),
    path("recoverpassword/", views.recoverpasswordPage.as_view(), name="recoverpassword"),
    path("project_add/", views.project_addPage.as_view(), name="project_add"),
    path("languagemenu/", views.languagemenuPage.as_view(), name="languagemenu"),
    path("pace/", views.pacePage.as_view(), name="pace"),
    path("project_edit/", views.project_editPage.as_view(), name="project_edit"),
    path("lockscreen/", views.lockscreenPage.as_view(), name="lockscreen"),
    path("invoiceprint/", views.invoiceprintPage.as_view(), name="invoiceprint"),
    path("jsgrid/", views.jsgridPage.as_view(), name="jsgrid"),
    path("data/", views.dataPage.as_view(), name="data"),
    path("simple/", views.simplePage.as_view(), name="simple"),
    path("readmail/", views.readmailPage.as_view(), name="readmail"),
    path("mailbox/", views.mailboxPage.as_view(), name="mailbox"),
    path("compose/", views.composePage.as_view(), name="compose"),
    path("ribbons/", views.ribbonsPage.as_view(), name="ribbons"),
    path("buttons/", views.buttonsPage.as_view(), name="buttons"),
    path("timeline/", views.timelinePage.as_view(), name="timeline"),
    path("navbar/", views.navbarPage.as_view(), name="navbar"),
    path("icons/", views.iconsPage.as_view(), name="icons"),
    path("general/", views.generalPage.as_view(), name="general"),
    path("modals/", views.modalsPage.as_view(), name="modals"),
    path("sliders/", views.slidersPage.as_view(), name="sliders"),

]



