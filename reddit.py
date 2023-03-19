import praw
import requests

# Define suas credenciais de API do Reddit
client_id = "id"
client_secret = "secret"
username = "user"
password = "pass"
user_agent = "testing_api by /u/yourusergoeshere"

# Cria uma nova instância da API do Reddit
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Define as subreddits onde você deseja postar
subreddits = ["Subname1", "Subname2"]

# Define as URLs das imagens que você deseja postar
image_urls = [
  "Link1", 
  "Link2"
]

# Mantém um registro das subreddits que não puderam receber um post
failed_subreddits = []

# Tenta postar as imagens em cada subreddit especificado
for subreddit_name in subreddits:
    try:
        subreddit = reddit.subreddit(subreddit_name)
        for image_url in image_urls:
            response = requests.head(image_url)
            if response.status_code == 200:
                submission = subreddit.submit(title="textoaqui", url=image_url)
                if submission.link_flair_text is None and subreddit.flair_enabled:
                    flairs = subreddit.flair.link_templates
                    if len(flairs) > 0:
                        submission.flair.select(flairs[0]['flair_template_id'])
                break
        else:
            print("Nenhuma imagem válida encontrada para a subreddit {}".format(subreddit_name))
            failed_subreddits.append(subreddit_name)
    except AttributeError:
        print("A subreddit {} não tem suporte a flairs, postando normalmente".format(subreddit_name))
        for image_url in image_urls:
            response = requests.head(image_url)
            if response.status_code == 200:
                subreddit.submit(title="textoaqui", url=image_url)
                break
        else:
            print("Nenhuma imagem válida encontrada para a subreddit {}".format(subreddit_name))
            failed_subreddits.append(subreddit_name)
    except Exception as e:
        print("Erro ao postar na subreddit {}: {}".format(subreddit_name, str(e)))
        failed_subreddits.append(subreddit_name)
        continue

# Imprime a lista de subreddits que não puderam receber um post
if len(failed_subreddits) > 0:
    print("Não foi possível postar em algumas subreddits:")
    for subreddit_name in failed_subreddits:
        print("- {}".format(subreddit_name))
    with open("failed_subreddits.txt", "w") as f:
        f.write("\n".join(failed_subreddits))
    print("A lista de subreddits que não puderam receber um post foi salva em 'failed_subreddits.txt'.")
else:
    print("Postagem concluída")
