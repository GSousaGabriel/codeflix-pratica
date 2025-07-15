import time

def wait_for_video_update(repo, video_id, expected_status="COMPLETED", timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        video = repo.get_by_id(video_id).video
        if video and video.status == expected_status:
            return video
        time.sleep(0.1)
    raise TimeoutError("Timed out waiting for video to be updated by consumer")
