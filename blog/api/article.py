from flask_combo_jsonapi import ResourceList, ResourceDetail
from combojsonapi.event.resource import EventsResource

from blog.schemas import ArticleSchema
from blog.extension import db
from blog.models import Article



class ArticleEvent(EventsResource):

    def event_get_count(self):
        return {"count": Article.query.count()}
    

class ArticleList(ResourceList):
    events = ArticleEvent
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
    }


