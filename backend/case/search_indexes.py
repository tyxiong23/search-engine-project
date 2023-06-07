from haystack import indexes
from case.models import Case

class CaseIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段，必须这么写
    text = indexes.CharField(document=True, use_template=True)

    # 模型字段，打包数据
    id = indexes.IntegerField(model_attr="id")
    qw_value = indexes.CharField(model_attr="qw_value")
    head = indexes.CharField(model_attr="head")
    note_name = indexes.CharField(model_attr="note_name")
    judge_prop = indexes.CharField(model_attr="judge_prop")
    court = indexes.CharField(model_attr="court")
    case_reason = indexes.CharField(model_attr="case_reason")
    province = indexes.CharField(model_attr="province")
    year = indexes.IntegerField(model_attr="year")
    

    def get_model(self):
        return Case

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
