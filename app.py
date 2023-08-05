from flask import Flask, request, send_file, jsonify, after_this_request
from pytube import YouTube
import moviepy.editor as mp
import json
import os
import io

app = Flask(__name__)


@app.route('/')
def index():
    try:
        video_id = request.args.get('id')
        yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
        # Altere a resolução conforme desejado
        video_stream = yt.streams.filter(res="720p").first()

        if not video_stream:
            return jsonify({"error": "Stream de vídeo não encontrado."})

        start_time = request.args.get('start')
        end_time = request.args.get('end')
        print("Recortando o vídeo...")
        video_clip = mp.VideoFileClip(
            video_stream.url).subclip(start_time, end_time)

        output_video_path = "./temp/" + video_id + "_output_video.mp4"
        video_clip.write_videofile(output_video_path)

        # print("Recortando o áudio...")
        # audio_clip = video_clip.audio
        # output_audio_path = "JS1R6GvbqOwoutput_audio.mp3"
        # audio_clip.write_audiofile(output_audio_path)

        video_clip.close()
        # audio_clip.close()

        print("Download concluído!")

        # Remove os arquivos temporários após a resposta ser enviada
        @after_this_request
        def remove_temp_files(response):
            try:
                os.remove(output_video_path)
                # os.remove(output_audio_path)
            except Exception as e:
                print("Erro ao remover arquivos temporários:", e)
            return response

        # Lê o arquivo de vídeo e envia para o cliente
        with open(output_video_path, 'rb') as video_file:
            video_data = video_file.read()
            response = send_file(
                io.BytesIO(video_data),
                as_attachment=True,
                mimetype="video/mp4",
                download_name= video_id + "output_video.mp4"
            )
            response.headers["Content-Disposition"] = "attachment; filename=" + video_id + "_output_video.mp4"
            return response

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run()


# from flask import Flask, request, jsonify
# from chat_downloader import ChatDownloader
# from pytube import YouTube
# import gc
# import json

# app = Flask(__name__)

# request_counter = 0  # Contador de requisições

# @app.after_request
# def cleanup(response):
#     global request_counter

#     # Incrementa o contador de requisições
#     request_counter += 1

#     # Limpa a memória a cada 5 requisições
#     if request_counter % 5 == 0:
#         gc.collect()

#     return response


# @app.get('/')
# def index():
#     try:
#         video = YouTube(f'https://www.youtube.com/watch?v=' + request.args.get('id'))

#         # Obter dados do vídeo
#         title = video.title
#         thumb = video.thumbnail_url
#         publish_date = video.publish_date
#         views = video.views
#         duration = video.length

#         # Obter dados do canal
#         channel_title = video.author


#         chat = ChatDownloader().get_chat("https://www.youtube.com/watch?v=" + request.args.get('id'), message_groups=['messages', 'superchat'])
#         chat_data = []
#         for message in chat:
#             message["author"]["images"] = message["author"]["images"][2]["url"]

#             if "badges" in message["author"]:
#                 message["author"]["badges"] = message["author"]["badges"][0]["title"]

#             # if "emotes" in message:
#             #     del message["emotes"]

#             # if "message_type" in message:
#             #     del message["message_type"]

#             # if "action_type" in message:
#             #     del message["action_type"]

#             chat_data.append(message)

#         data = {
#             "video": {
#                 "title": title,
#                 "publish_date": publish_date,
#                 "views": views,
#                 "channel_title": channel_title,
#                 "thumb": thumb,
#                 "duration": duration
#             },
#             "chat": chat_data
#         }
#         return jsonify(data)
#     except Exception as e:
#         return json.dumps({"error": str(e)}, ensure_ascii=False)


# if __name__ == '__main__':
#         app.run()
