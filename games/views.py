from django.shortcuts import redirect, get_object_or_404
from .models import Game, Review
from .forms import ReviewForm
from django.views import generic

class GameList(generic.ListView):
    model = Game
    queryset = Game.objects.all()
    template_name = 'games/game_list.html'
    context_object_name = 'games'

class GameDetail(generic.DeleteView):
    model = Game
    template_name = 'games/game_detail.html'
    context_object_name = 'game'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()
        context['reviews'] = game.reviews.all().order_by('-created_at')
        context['form'] = kwargs.get('form') or ReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = self.object
            review.save()
            return redirect('game_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))
    