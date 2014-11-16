from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from text_markup import markup
from text_markup.special_formatters import format_references


class Post(models.Model):
    """Base class for both OP-posts and replies."""

    name = models.CharField(blank=True, default='Anonymous', max_length=70)
    subj = models.CharField(blank=True, max_length=200)
    text = models.TextField(max_length=3000)

    picture = models.ImageField(upload_to='pics/', blank=True, null=True)
    picture_thumbnail = ImageSpecField(source='picture',
                                       processors=[ResizeToFit(300, 300)],
                                       format='JPEG',
                                       options={'quality': 85})

    pub_date = models.DateTimeField(auto_now_add=True)
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return(self.subj if self.subj else (
            self.text[:200]+'...' if len(self.text) > 200 else self.text))
        # post subject if there's one or cutten post text


class Thread(Post):
    last_bumped = models.DateTimeField(null=True, blank=True, default=None)

    def save(self, *args, **kwargs):

        # manually incrementing post id
        if not self.id:
            self.id = 1
            if Thread.objects.all():
                # for case there's at least one thread
                # and at least one reply to compare with
                if Reply.objects.all():

                    self.id = max(
                        Thread.objects.last().id,
                        Reply.objects.last().id,) + 1
                else:
                    self.id = Thread.objects.last().id + 1

        super(Thread, self).save()

        # manually setting last_bumped value
        if not self.last_bumped:
            self.update_last_bumped()

        self.format_text()

    def update_last_bumped(self):

        if self.reply_set.last():  # if thread has at least one reply
            self.last_bumped = self.reply_set.last().pub_date
        else:
            self.last_bumped = self.pub_date

        super(Thread, self).save()

    def format_text(self):
        self.text = markup.get_markup(self.text)
        self.text = format_references(self.text)

        super(Thread, self).save()

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return(reverse('board:thread', kwargs={'pk': str(self.id)}))

    def get_last_replies(self, amount=5):
        return(self.reply_set.order_by('-id')[:amount:-1])


class Reply(Post):
    thread = models.ForeignKey(Thread)
    sage = models.BooleanField(blank=True, default=False)

    def save(self, *args, **kwargs):

        if not self.id:

            if Reply.objects.all():
                # for case there's at least one reply to compare with
                # (if we're creating a reply, there are already should be the
                # thread we want to reply to, so counting threads is pointless)

                self.id = max(
                    Thread.objects.last().id,
                    Reply.objects.last().id,) + 1

            else:
                self.id = Thread.objects.last().id + 1

        super(Reply, self).save()

        if not self.sage:
            self.thread.update_last_bumped()

        self.format_text()

    def format_text(self):
        self.text = markup.get_markup(self.text)
        self.text = format_references(self.text)

        super(Reply, self).save()
