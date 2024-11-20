import random
import time
from groq import Groq

#SỬ dụng api free groq/ để đạt performance tốt nhất vẫn nên sử dụng api openai
class Request:
    TOKEN_LIMIT = 500000  # Giới hạn token của groq API

    def __init__(self, api_keys, model):
        """
        Khởi tạo đối tượng Request.
        :param api_keys: List các API keys để sử dụng.
        :param model: Tên mô hình.
        """
        self.api_keys = api_keys
        self.current_key_index = 0
        self.model = model
        self.cumulative_tokens_used = 0  # Tổng số token đã sử dụng cho toàn bộ chương trình
        self.token_usage = [0] * len(api_keys)  # Danh sách token đã sử dụng cho từng API key
        self.holder = Groq(api_key=self.api_keys[self.current_key_index])

    def _rotate_api_key(self):
        """
        Chuyển sang API key tiếp theo trong danh sách.
        """
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        self.holder = Groq(api_key=self.api_keys[self.current_key_index])
        print(f"Switched to API key index: {self.current_key_index}")

    def _check_and_rotate_key(self):
        """
        Kiểm tra nếu API key hiện tại đã đạt giới hạn và chuyển key nếu cần.
        """
        if self.token_usage[self.current_key_index] >= self.TOKEN_LIMIT:
            print(f"API key index {self.current_key_index} reached token limit. Switching to next key.")
            self._rotate_api_key()

    def request(self, user, system=None, message=None):
        """
        Gửi yêu cầu đến API và xử lý phản hồi.
        
        :param user: Nội dung từ phía người dùng.
        :param system: Nội dung từ phía hệ thống (nếu có).
        :param message: Thông điệp bổ sung (nếu có).
        :return: Nội dung phản hồi từ API.
        """
        self._check_and_rotate_key()
        response = self.groq_request(user, system, message)
        return response

    def groq_request(self, user, system=None, message=None):
        """
        Xử lý yêu cầu với API và retry nếu thất bại.
        
        :param user: Nội dung từ phía người dùng.
        :param system: Nội dung từ phía hệ thống (nếu có).
        :param message: Thông điệp bổ sung (nếu có).
        :return: Nội dung phản hồi từ API.
        """
        if system:
            messages = [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ]
        else:
            messages = [{"role": "user", "content": user}]

        # Thực hiện request với cơ chế retry
        for delay_secs in (2**x for x in range(0, 10)):  
            try:
                response = self.holder.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.2  
                )
                if isinstance(response, dict) and "choices" in response:
                    return response["choices"][0]["message"]["content"]
                elif hasattr(response, "choices"):
                    return response.choices[0].message.content
                else:
                    raise ValueError("Unexpected response format: Missing 'choices'")

            except Exception as e:
                print(f"Error: {e}. Retrying with next API key...")
                self._rotate_api_key()
                randomness_collision_avoidance = random.uniform(0, 1)
                sleep_dur = delay_secs + randomness_collision_avoidance
                print(f"Retrying in {round(sleep_dur, 2)} seconds.")
                time.sleep(sleep_dur)
                continue

        raise RuntimeError("All retries and API keys exhausted. Request failed.")
