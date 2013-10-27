from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import Q, Max
from django.template.defaultfilters import truncatechars
from kiqlist.notifications.utils import send_notification
from kiqlist.utils.views import ajax_form_view
from .models import PrivateMessage
from .forms import PrivateMessageForm, StartConversationForm


@login_required
def index(request):
	last_interlocutors = PrivateMessage.objects. \
		filter(Q(to_user=request.user) | Q(from_user=request.user)). \
		values("from_user", "to_user").annotate(max_created=Max("created")).order_by("-max_created")

	last_conversations = []
	for interlocutor in last_interlocutors:
		user1 = User.objects.get(id=interlocutor["from_user"])
		user2 = User.objects.get(id=interlocutor["to_user"])

		private_message = PrivateMessage.objects. \
			filter(Q(Q(to_user=user2) & Q(from_user=user1)) |
				   Q(Q(to_user=user1) & Q(from_user=user2))). \
			get(created=interlocutor["max_created"])

		last_conversations.append((private_message, user1))

	return render(request, "private_messages/index.html", {
		"last_conversations": last_conversations
	})


@login_required
def conversation(request, interlocutor_pk):
	interlocutor = get_object_or_404(User, pk=interlocutor_pk)
	private_messages = PrivateMessage.objects. \
		filter((Q(from_user=request.user) & Q(to_user=interlocutor)) | Q(Q(to_user=request.user) & Q(from_user=interlocutor))).order_by("created")

	return render(request, "private_messages/conversation.html", {
		"interlocutor": interlocutor,
		"private_messages": private_messages,
		"form": PrivateMessageForm()
	})


@login_required
def add_private_message(request):
	if request.method == "POST":
		form = PrivateMessageForm(request.POST)
		if form.is_valid():
			private_message = form.save(commit=False)
			private_message.from_user = request.user
			private_message.save()

			send_notification(private_message.to_user,
							  "%s %s sent you a message \"%s\"." % (request.user.first_name,
																  request.user.last_name,
																  truncatechars(private_message.content, 50)),
							  "#pm/conversation/" + str(request.user.pk))

			return redirect("kiqlist.private_messages.views.conversation", private_message.to_user.pk)

	return redirect("private_messages.views.index")


@login_required
def start_conversation(request, template="private_messages/start_conversation_form.html"):
	def success(form):
		return form.user

	return ajax_form_view(request, StartConversationForm, success, template)
