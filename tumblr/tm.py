import pytumblr
import sys
import os
import configparser
import optparse
import datetime
import logging


class tumblr():
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.tumblr_client = pytumblr.TumblrRestClient(
            config['tumblr']['consumer'],
            config['tumblr']['secret'],
            config['tumblr']['token'],
            config['tumblr']['token_secret']
        )
        self.blogName = config['tumblr']['blog_name']

        user_info = self.tumblr_client.info()
        if user_info['user']['name'] != self.blogName:
            logging.debug('api key get blog name: %s , config blog name : %s' %
                  (user_info['user']['name'], self.blogName))
            sys.exit(1)
        logging.debug('blog name :%s , blog url : %s' %
              (user_info['user']['name'], user_info['user']['blogs'][0]['url']))


# Creates a photo post from local file
# client.create_photo(blogName, state="private", tags=["testing", "ok"],
#                     data=["/tmp/tumblr_n55vdeTse11rn1906o1_500.jpg"])

    def create_video(self, title: str, video_file: str, tags: list, state: str):
        # Creating a video post from local file
        logging.info('start upload video ,title %s' % title)
        s = self.tumblr_client.create_video(
            self.blogName, state=state, caption=title, data=video_file, tags=tags)
        logging.info('Video id : %s' % s.get('id'))

    def create_text(self, title: str, body: str, tags: list, state: str):
        # Creating a text post
        logging.info('create text title %s' % title)
        s = self.tumblr_client.create_text(
            self.blogName, state=state, title=title, body=body, tags=tags)
        logging.info('Post id : %s' % s.get('id'))
# client.edit_post(blogName, id=post_id, type="text", title="Updated")
# print('edit text post')
# post_id = s.get('id')
# client.edit_post(blogName, id=post_id, type="video", body='test edit body')


def run_main(parser, options, args):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tags = options.tags.split(",")
    client = tumblr(options.config_file)
    if options.title_template:
        title_template = '{date_time} {title}'
        d = {'date_time': now, 'title': options.title}
        complete_title = title_template.format(**d)
    client.create_video(complete_title, options.video_file,
                        tags, options.state)

    # post text
    text_title = '%s text' % complete_title
    if options.body_file:
        with open(options.body_file, 'r') as f:
            body = f.read().decode('utf-8')
        client.create_text(text_title, body, tags, options.state)
    elif options.post_body:
        body = options.post_body
        client.create_text(text_title, body, tags, options.state)


def main(arguments):
    """Upload videos to tumblr."""
    usage = """Usage: %prog [OPTIONS] ]

    Upload videos to tumblr."""
    parser = optparse.OptionParser(usage)

    # Video metadata
    parser.add_option('-t', '--title', dest='title', type="string",
                      help='Video title')

    parser.add_option('-f', '--video-file', dest='video_file', type="string",
                      help='Video file')

    parser.add_option('', '--body-file', dest='body_file', type="string",
                      help='Post body file', default=None)

    parser.add_option('', '--post-body', dest='post_body', type="string",
                      help='Post body file', default=None)

    parser.add_option('', '--tags', dest='tags', type="string",
                      help='Video tags (separated by commas: "tag1, tag2,...")')
    parser.add_option('', '--state', dest='state', metavar="STRING",
                      default="private", help='State status (published | draft | queue | private)')

    parser.add_option('', '--title-template', dest='title_template',
                      default=True, action='store_false',
                      help='Use template for video ( {date_time} {title} )')

    # parser.add_option('-f', '--video_file', dest='video_file',
    #                   type='string', help='video file path')

    # Authentication

    parser.add_option('-c', '--config-file', dest='config_file', type="string",
                      help='config file', default=None)

    parser.add_option('', '--debug', dest='debug', default=False,
                      action='store_true', help='Print debug log')

    options, args = parser.parse_args(arguments)

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %p"
    if options.debug:
        logging.basicConfig(level=logging.DEBUG,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)
    logging.info('start')
    run_main(parser, options, args)



if __name__ == '__main__':

    main(sys.argv[1:])
