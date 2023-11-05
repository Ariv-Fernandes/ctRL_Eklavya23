from mmap import mmap
import numpy as np


class AgentHost:
    def __init__(self, obs_filename: str, act_filename: str) -> None:
        self.obs_file = open(obs_filename, 'rb+')
        self.act_file = open(act_filename, 'rb+')

        self.obs_buffer = mmap(self.obs_file.fileno(), 0)
        self.act_buffer = mmap(self.act_file.fileno(), 0)

    def __del__(self) -> None:
        self.obs_buffer.close()
        self.act_buffer.close()

        self.obs_file.close()
        self.act_file.close()

    def get_observation_from_sim(self) -> np.ndarray:
        return np.frombuffer(self.obs_buffer, dtype=np.float64)
    
    def pass_action_to_sim(self, action: np.ndarray) -> None:
        self.act_buffer.write(action.tobytes())
        self.act_buffer.seek(0)
        # self.act_buffer.flush()


class SimHost:
    def __init__(self, obs_filename, act_filename) -> None:
        self.obs_file = open(obs_filename, 'rb+')
        self.act_file = open(act_filename, 'rb+')

        self.obs_buffer = mmap(self.obs_file.fileno(), 0)
        self.act_buffer = mmap(self.act_file.fileno(), 0)

    def __del__(self) -> None:
        self.obs_buffer.close()
        self.act_buffer.close()

        self.obs_file.close()
        self.act_file.close()

    def pass_observation_to_agent(self, observation: np.ndarray) -> None:
        self.obs_buffer.write(observation.tobytes())
        self.obs_buffer.seek(0)
        # self.obs_buffer.flush()

    def get_action_from_agent(self) -> np.ndarray:
        return np.frombuffer(self.act_buffer, dtype=np.float64)
