# squad_detector.py
class SquadDetector:
    @staticmethod
    def find_slot23(data):
        best_start = None
        best_cnt = 0
        limit = min(len(data), 1024*1024)
        for start in range(0, limit - 46, 2):
            cnt = 0
            for i in range(23):
                off = start + i*2
                pid = data[off] | (data[off+1] << 8)
                if 1 <= pid <= 5000:
                    cnt += 1
            if cnt > best_cnt:
                best_cnt = cnt
                best_start = start
                if cnt >= 20:
                    break
        return best_start

    @staticmethod
    def find_slot32(data):
        best_start = None
        best_cnt = 0
        limit = min(len(data), 1024*1024)
        for start in range(0, limit - 64, 2):
            cnt = 0
            for i in range(32):
                off = start + i*2
                pid = data[off] | (data[off+1] << 8)
                if 1 <= pid <= 5000:
                    cnt += 1
            if cnt > best_cnt:
                best_cnt = cnt
                best_start = start
                if cnt >= 20:
                    break
        return best_start