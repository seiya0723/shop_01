from django.db import models
from django.utils import timezone

import uuid 


class ProductCategory(models.Model):
    
    #本格的な運用を試みるのであれば、自動採番で予測されやすい数値型の主キーではなく、不規則な文字列が生成されるUUID型の主キーを使用するとセキュリティが向上する。
    #https://ja.wikipedia.org/wiki/UUID

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="登録日時",default=timezone.now)

    name    = models.CharField(verbose_name="カテゴリ名",max_length=20)


    def __str__(self):
        return self.name

"""
class ProductTag(models.Model):

    id      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt      = models.DateTimeField(verbose_name="登録日時",default=timezone.now)

    name    = models.CharField(verbose_name="タグ名",max_length=20)

    def __str__(self):
        return self.name
"""


class Product(models.Model):

    #同じカテゴリと同じ商品名の組み合わせの登録は禁止にする。unique_togetherを使用する。
    #例:名前の重複を禁止する場合、便箋用の『マスキングテープ』と工具用の『マスキングテープ』が同時に登録できないため、カテゴリと名前の組み合わせでの重複を禁止にする。
    #https://noauto-nolife.com/post/django-same-user-operate-prevent/

    
    class Meta:
        unique_together = ("category","name")


    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="登録日時", default=timezone.now)

    category    = models.ForeignKey(ProductCategory, verbose_name="カテゴリ", on_delete=models.PROTECT)
    name        = models.CharField(verbose_name="商品名", max_length=100)
    
    #価格にマイナスはありえないので、正の整数だけを受け付けるPositiveIntegerFieldを使用する。
    price       = models.PositiveIntegerField(verbose_name="価格")


    #タグ。descriptionにハッシュタグ含めて使うのであれば、この多対多は不要
    #多対多:https://noauto-nolife.com/post/django-many-to-many/
    #ハッシュタグ:https://noauto-nolife.com/post/django-custom-template-tags-hashtags/
    #tags        = models.ManyToManyField(ProductTag,verbose_name="タグ")


    #多対多の用途は？
    #ElementTubeのmodels.pyにて、動画のマイリストなどに使われている。
    #https://github.com/seiya0723/elementtube/blob/master/tube/models.py
    #通販サイトであれば、お気に入り登録などがそれに当てはまると思われる。ただし、ユーザーモデルの内容をやった上で実装したほうが良い。


    #1対多で関連づいた画像を全て取り出し、モデルオブジェクトのリストを返却。テンプレートではこれをループして1枚ずつ画像を出す。
    def images(self):
        return ProductImage.objects.filter(product=self.id).order_by("-dt")


    def __str__(self):
        return self.name


class ProductImage(models.Model):

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dt          = models.DateTimeField(verbose_name="登録日時", default=timezone.now)

    #スネークケースでアプリ名/モデルクラス名/フィールド名に保存する。
    image       = models.ImageField(verbose_name="商品画像", upload_to="shop/product_image/image/")

    #画像を指定する。1対多を使う。
    #理由:商品に指定する画像の個数は、後からフレキシブルに変更できるようにする必要がある。そのため、ProductにImageFieldを複数追加する方法は望ましくない。
    product     = models.ForeignKey(Product,verbose_name="対象商品",on_delete=models.CASCADE)




