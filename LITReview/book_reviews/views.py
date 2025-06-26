from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm, SearchUserForm
from django.contrib import messages
from book_reviews.models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def home(request):
    return render(request, "book_reviews/home.html")


@login_required
def search_user(request):
    form = SearchUserForm(request.GET)
    searched = False
    user_following = request.user.following.values_list('followed_user__id', flat=True)
    user_follower = request.user.followed_user.values_list('followed_by', flat=True)

    if form.is_valid():
        searched = True
        user_searched = form.cleaned_data["user_searched"]
        followed_user = request.user.following.values_list('followed_user__id', flat=True)
        found_user = User.objects.filter(username__icontains=user_searched).exclude(id=request.user.id, id__in=followed_user)
        if not found_user.exists():
            messages.info(request, f"Aucun utilisateur touvé pour : {user_searched}.")
        
    else:
        searched = True
        messages.error(request, f"Recherche non valide.")

    context = {
        "form": form,
        "found_user": found_user,
        "searched": searched,
        "user_following": user_following,
        "user_follower": user_follower,
    }
    return render(request, "book_review/follow.html", context)


@login_required
def follow_action(request):
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "follow":
            follow_user_id = request.POST.get("followed_user_id")
            try:
                followed_user = User.objects.get(id=follow_user_id)
            except:
                messages.error(request, "L'utilisateur n'existe pas.")
                return redirect("manage_users")
            
            if followed_user == request.user:
                messages.error(request, "Vous ne pouvez pas vous suivre vous-même !")
                return redirect("manage_users")

            if UserFollows.objects.filter(user=request.user, followed_user=followed_user).exists():
                messages.info(request, f"Vous suivez déja {followed_user.username} !")

            follow = UserFollows(user= request.user, followed_user=followed_user)
            follow.save()
            messages.success(request, f"Vous suivez maintenant {followed_user.username}.")
            return redirect("manage_users")

        elif action == "unfollow":
            unfollow_user_id = request.POST.get("unfollow_user_id")
            try:
                unfollow_user = User.objects.get(id=unfollow_user_id)
            except:
                messages.error(request, "L'utilisateur n'existe pas.")
                return redirect("manage_users")
            
            UserFollows.objects.filter(user=request.user, followed_user=unfollow_user).delete()
            messages.success(request, f"Vous ne suivez plus {unfollow_user.username}")

    return render(request, "book_reviews/follow.html")


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Votre ticket a été crée !")
            return redirect('home')
    else:
        form = TicketForm()

    return render(request, "book_reviews/create_ticket.html", {"form": form})


@login_required
def update_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier ce billet.")
        return redirect("home")

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre billet a été modifié avec succès !")
            return redirect("home")
        
    else:
        form = TicketForm(instance=ticket)
    
    context = {"form":form, "ticket": ticket}
    return render(request, "book_reviews/update_ticket.html", context)


@login_required
def delete_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if ticket.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer ce billet.")
        return redirect("home")
    
    if request.method == "POST":
        ticket.delete()
        return redirect('post')

    context = {"ticket": ticket}
    return render(request, "book_reviews/delete_ticket.html", context)


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "Votre critique a été crée !")
            return redirect('home')
    else:
        form = ReviewForm()

    context = {"form": form, "ticket": ticket}
    return render(request, "book_reviews/create_review.html", context)


@login_required
def update_review(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette critique.")
        return redirect("home")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a été modifié avec succès !")
            return redirect("home")
        
    else:
        form = ReviewForm(instance=review)
        
    context = {"form":form, "review": review, "ticket": review.ticket}
    return render(request, "book_reviews/update_review.html", context)


@login_required
def delete_review(request, id):
    review = get_object_or_404(Review, id=id)

    if review.user != request.user:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette critique.")
        return redirect("home")
    
    if request.method == "POST":
        review.delete()
        return redirect('post')

    context = {"review": review}
    return render(request, "book_reviews/delete_review.html", context)


@login_required
def create_ticket_and_review(request):
    ticket_form = TicketForm()
    review_form = ReviewForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if all([ticket_form.is_valid(), review_form.is_valid()]):
            ticket = ticket_form.save(comit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(comit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "Billet et critique créés avec succès !")

    context = {"ticket_form": ticket_form, "review_form": review_form}
    return render(request, "book_reviews/create_ticket_and_review.html", context)
