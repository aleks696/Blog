from django.db import models


class Post(models.Model):
    title       = models.CharField('Title', max_length=100)
    description = models.TextField('Description')
    tags        = models.CharField(max_length=200, )
    city        = models.CharField(max_length=255)
    author      = models.CharField('Author', max_length=100)
    date        = models.DateTimeField('Date', auto_now_add=True)
    img         = models.ImageField('Image',
                                    upload_to='image/%Y')

    def __str__(self):
        return f'{self.title}, {self.author}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

class Comments(models.Model):
    email         = models.EmailField()
    name          = models.CharField('Name', max_length=50)
    text_comments = models.TextField("Comment", max_length=2000)
    post          = models.ForeignKey(Post, verbose_name="Post",
                             on_delete=models.CASCADE)
    parent        = models.ForeignKey('self', null=True, blank=True,
                             related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.post}'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

class Likes(models.Model):
    ip = models.CharField(max_length=100)
    pos = models.ForeignKey(Post, verbose_name="Post",
                                  on_delete=models.CASCADE)
