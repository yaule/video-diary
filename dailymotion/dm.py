import dailymotion
# pip3 install dailymotion
import sys
import os
import configparser
import optparse
import datetime
import logging


class daily_motion():
    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        logging.info('config file : %s' % config_file)
        self.config.read(config_file)
        self.d = dailymotion.Dailymotion()
        self.d.set_grant_type('password', api_key=self.config['dailymotion']['api_key'], api_secret=self.config['dailymotion']['api_secret'],
                              scope=['manage_videos'], info={'username': self.config['dailymotion']['username'], 'password': self.config['dailymotion']['password']})
        logging.debug('%s' % self.d.get('/me'))
        logging.info('%s' % self.d.get('/me', {'fields': 'id'}))

    def upload_video(self, title, video_file, channel, privacy, for_kids='false'):
        logging.info('%s' % title)
        logging.info('upload videl start : %s ' % video_file)
        url = self.d.upload(video_file)
        self.d.post(
            "/me/videos",
            {
                "url": url,
                "title": title,
                "published": privacy,
                "channel": channel,  # "lifestyle",
                "is_created_for_kids": for_kids,
            },
        )


def run_main(parser, options, args):
    dm = daily_motion(options.config_file)

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tags = options.tags.split(",")
    if options.title_template:
        title_template = '{date_time} {title}'
        d = {'date_time': now, 'title': options.title}
        complete_title = title_template.format(**d)

    # upload video
    text_title = '%s' % complete_title
    dm.upload_video(text_title, options.video_file,
                    options.channel, options.privacy)


def main(arguments):
    """Upload videos to dailymotion."""
    usage = """Usage: %prog [OPTIONS]]

    Upload videos to dailymotion."""
    parser = optparse.OptionParser(usage)

    # Video metadata
    parser.add_option('-t', '--title', dest='title', type="string", default='test daily notes',
                      help='Video title')

    parser.add_option('-f', '--video-file', dest='video_file', metavar="FILE",
                      help='Video file')

    parser.add_option('', '--channel', dest='channel', type='string', default='lifestyle',
                      help='channel')

    parser.add_option('', '--tags', dest='tags', type="string", default='daily_note',
                      help='Video tags (separated by commas: "tag1, tag2,...")')
    parser.add_option('', '--privacy', dest='privacy', metavar="STRING",
                      default='false', help='published status ')

    parser.add_option('', '--title-template', dest='title_template',
                      default=True, action='store_false',
                      help='Use template for video ( {date_time} {title} )')

    # Authentication

    parser.add_option('-c', '--config-file', dest='config_file', metavar="FILE", default='config.ini',
                      help='config file')

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
