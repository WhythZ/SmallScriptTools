import os
import subprocess
import sys

def get_video_duration(video_path):
    """使用FFmpeg获取视频时长（秒）"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to get video duration: {e.stderr}")
        return None
    except FileNotFoundError:
        print("ERROR: FFmpeg/FFprobe not found. Please install FFmpeg first.")
        return None

def split_video(video_path, n, output_dir=None):
    """将视频等分为n份，传入视频文件的绝对路径以及输出产物路径（默认与原视频同目录）"""
    # 检查文件是否存在
    if not os.path.exists(video_path):
        print(f"ERROR: Video file '{video_path}' does not exist")
        return False

    if not os.path.isfile(video_path):
        print(f"ERROR: '{video_path}' is not a file")
        return False

    # 检查n值
    if n <= 0:
        print(f"ERROR: n must be a positive integer, got {n}")
        return False

    # 获取视频时长
    print("Getting video duration...")
    duration = get_video_duration(video_path)
    if duration is None:
        return False

    print(f"Video duration: {duration:.2f} seconds")

    # 计算每段时长
    segment_duration = duration / n
    print(f"Each segment will be approximately {segment_duration:.2f} seconds")

    # 确定输出目录
    if output_dir is None:
        output_dir = os.path.dirname(video_path)
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取原文件名（不带扩展名）
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    ext = os.path.splitext(video_path)[1]

    # 分割视频
    print(f"\nSplitting video into {n} parts...")
    success_count = 0
    failed_segments = []

    for i in range(n):
        start_time = i * segment_duration

        # 生成输出文件名
        output_file = os.path.join(output_dir, f"{base_name}_part{i+1:02d}{ext}")

        # 检查文件是否已存在
        if os.path.exists(output_file):
            response = input(f"File '{output_file}' already exists. Overwrite? (y/n): ")
            if response.lower() != 'y':
                print(f"Skipping segment {i+1}")
                failed_segments.append((i + 1, "File already exists"))
                continue

        # 使用FFmpeg分割
        # 使用-ss在-i之前更快，但可能不够精确
        # 使用-c copy可以避免重新编码，速度更快
        cmd = [
            'ffmpeg',
            '-y',  # 覆盖输出文件
            '-ss', str(start_time),
            '-i', video_path,
            '-t', str(segment_duration),
            '-c', 'copy',  # 直接复制流，不重新编码
            '-avoid_negative_ts', '1',  # 避免负时间戳问题
            output_file
        ]

        print(f"Creating part {i+1}/{n}...")

        try:
            # 运行FFmpeg，捕获输出但显示进度
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore'
            )

            # 实时显示FFmpeg输出
            for line in process.stdout:
                # 简单的进度显示
                if 'time=' in line:
                    print(f"\rPart {i+1}/{n} - {line.strip()}", end='', flush=True)

            process.wait()

            if process.returncode == 0:
                success_count += 1
                print(f"\n✓ Part {i+1} created: {output_file}")
            else:
                failed_segments.append((i + 1, "FFmpeg error"))
                print(f"\n✗ Part {i+1} failed")

        except FileNotFoundError:
            print("\nERROR: FFmpeg not found. Please install FFmpeg first.")
            return False
        except Exception as e:
            failed_segments.append((i + 1, str(e)))
            print(f"\n✗ Part {i+1} failed: {e}")

    # 显示结果
    print(f"\n{'='*60}")
    print(f"Splitting completed: {success_count}/{n} parts created")

    if failed_segments:
        print("\nFailed segments:")
        for part_num, error in failed_segments:
            print(f"  Part {part_num}: {error}")

    # 显示输出文件信息
    if success_count > 0:
        print(f"\nOutput directory: {output_dir}")
        for i in range(n):
            output_file = os.path.join(output_dir, f"{base_name}_part{i+1:02d}{ext}")
            if os.path.exists(output_file):
                size_mb = os.path.getsize(output_file) / (1024 * 1024)
                print(f"  {os.path.basename(output_file)}: {size_mb:.2f} MB")

    return success_count > 0

def do_prepare():
    """准备参数并执行分割"""
    print("="*60)
    print("Video Splitter - Split video into N parts using FFmpeg")
    print("="*60)

    # 获取视频路径
    video_path = input("\nInput the absolute path of the video file (.mp4): ").strip()
    if not video_path:
        print("ERROR: Video path cannot be empty")
        return

    # 获取分割份数
    n_input = input("Input the number of parts (n): ").strip()
    if not n_input:
        print("ERROR: n cannot be empty")
        return

    try:
        n = int(n_input)
    except ValueError:
        print("ERROR: n must be an integer")
        return

    # 获取输出目录（可选）
    output_dir = input("Input output directory (leave empty to use same directory as video): ").strip()
    if not output_dir:
        output_dir = None

    # 执行分割
    split_video(video_path, n, output_dir)

if __name__ == "__main__":
    try:
        # 重复执行，直到用户Ctrl+C退出
        while True:
            do_prepare()
            print("\n" + "="*60 + "\n")
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user")
    except Exception as e:
        print(f"\nProgram interrupted by error: {str(e)}")