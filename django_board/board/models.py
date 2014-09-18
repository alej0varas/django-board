from django.db import models


class Post(models.Model):
    """Base class for both OP-posts and replies."""

    name = models.CharField(blank=True, default='Anonymous', max_length=70)
    subj = models.CharField(blank=True, max_length=200)
    text = models.TextField(max_length=3000)
    pub_date = models.DateTimeField(auto_now_add=True)

    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True

    def __str__(self):
        return(self.subj if self.subj else (
            self.text[:200]+'...' if len(self.text) > 200 else self.text))
        # post subject if there's one or cutten post text


class Thread(Post):

    def save(self, *args, **kwargs):

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


class Reply(Post):
    thread = models.ForeignKey(Thread)

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
