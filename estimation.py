"""
Functions for estimating expected scores based on rating (prior) and head-to-head score (posterior)
"""


def prior(player, opponent, time_control):
    if time_control == "Classical":
        return 1/(1 + 10**((opponent.rating - player.rating)/400))
    elif time_control == "Rapid":
        return 1/(1 + 10**((opponent.rapid - player.rapid)/400))
    elif time_control == "Blitz":
        return 1/(1 + 10**((opponent.blitz - player.blitz)/400))


def posterior(player, opponent, time_control):
    if time_control == "Rapid" or time_control == "Blitz":
        time_control = "RapidBlitz"
    score = player.scores[time_control][opponent.name]
    points = score[0] + score[2]/2
    game_count = sum(score)
    
    return points/game_count, game_count


def bayes_estimate(prior, posterior, N, W):
    return (prior*W + posterior*N)/(W + N)


def estimate_score(player, opponent, W, time_control):
    p_prior = prior(player, opponent, time_control)
    p_posterior, n = posterior(player, opponent, time_control)
    
    return bayes_estimate(p_prior, p_posterior, n, W)


def calculate_rates(p):
    if p < 0.5:
        win_rate = p*0.4
        draw_rate = p*0.6*2
        loss_rate = 1 - win_rate - draw_rate
    else:
        loss_rate = (1-p)*0.4
        draw_rate = (1-p)*0.6*2
        win_rate = 1 - loss_rate - draw_rate
        
    return [win_rate, loss_rate, draw_rate]