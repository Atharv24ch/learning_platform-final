import unittest
from unittest.mock import patch, MagicMock
import sys
import importlib


class YouTubeHelperTests(unittest.TestCase):
	def test_search_youtube_videos_returns_parsed_videos(self):
		# Mock response from the YouTube API
		sample_response = {
			'items': [
				{
					'id': {'kind': 'youtube#video', 'videoId': 'abc123'},
					'snippet': {
						'title': 'Test Video',
						'description': 'A test description',
						'thumbnails': {'high': {'url': 'http://thumb1'}},
						'channelTitle': 'Test Channel'
					}
				},
				# Non-video item should be ignored
				{
					'id': {'kind': 'youtube#channel', 'channelId': 'chan1'},
					'snippet': {}
				}
			]
		}

		mock_search = MagicMock()
		mock_search.list.return_value.execute.return_value = sample_response

		mock_build = MagicMock(return_value=MagicMock(search=MagicMock(return_value=mock_search)))

		# Ensure importing the youtube_helper doesn't fail if googleapiclient is absent
		fake_googleapiclient = MagicMock()
		fake_discovery = MagicMock()
		fake_googleapiclient.discovery = fake_discovery

		with patch.dict(sys.modules, {
			'googleapiclient': fake_googleapiclient,
			'googleapiclient.discovery': fake_discovery,
		}):
			# Load only the function source to avoid importing Django/DRF at module import
			import os
			module_path = os.path.join(os.path.dirname(__file__), 'youtube_helper.py')
			with open(module_path, 'r', encoding='utf-8') as f:
				src = f.read()

			# Extract the function definition for search_youtube_videos
			func_start = src.find('\ndef search_youtube_videos')
			if func_start == -1:
				self.fail('search_youtube_videos function not found in youtube_helper.py')

			# we'll take from the def line to the next top-level def/class or EOF
			tail = src[func_start+1:]
			stop_idx = len(tail)
			for marker in ('\nclass ', '\ndef '):
				i = tail.find(marker)
				if i != -1:
					stop_idx = min(stop_idx, i)

			func_src = tail[:stop_idx]

			# Prepare a globals dict with os and a placeholder for build
			import types
			mod_globals = {'os': __import__('os')}

			# Provide a dummy 'build' placeholder; we'll patch it on the function's module after exec
			# Execute the function source into mod_globals
			exec(func_src, mod_globals)

			# Now patch the 'build' name that the function will call
			with patch.dict(mod_globals, {'build': mock_build}):
				videos = mod_globals['search_youtube_videos']('test query', max_results=2)

		# Only one video item should be returned and fields mapped correctly
		self.assertEqual(len(videos), 1)
		v = videos[0]
		self.assertEqual(v['video_id'], 'abc123')
		self.assertEqual(v['title'], 'Test Video')
		self.assertEqual(v['description'], 'A test description')
		self.assertEqual(v['thumbnail'], 'http://thumb1')
		self.assertEqual(v['channel'], 'Test Channel')
		self.assertIn('embed_url', v)

