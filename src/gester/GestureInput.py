import threading
from gestures import GestureWrapper, GestureMessage

"""
public:
    init(dimensions) <- must be called first 
    close()

    get_hand_pos_x()
    get_hand_pos_y()
    get_hand_gesture()
    get_pointer_x()
    get_pointer_y()
"""

_lock = threading.Lock()
_hand_pos_x = -1
_hand_pos_y = -1
_pointer_x = -1
_pointer_y = -1
_hand_gesture = "NO_HAND"
_wrapper = None


def get_hand_pos_x():
    _lock.acquire()
    ret = _hand_pos_x
    _lock.release()
    return ret


def get_hand_pos_y():
    _lock.acquire()
    ret = _hand_pos_y
    _lock.release()
    return ret


def get_pointer_x():
    _lock.acquire()
    ret = _pointer_x
    _lock.release()
    return ret


def get_pointer_y():
    _lock.acquire()
    ret = _pointer_y
    _lock.release()
    return ret


def get_hand_gesture():
    _lock.acquire()
    ret = _hand_gesture
    _lock.release()
    return ret


def _process_data(data: GestureMessage):
    global _hand_pos_y, _hand_pos_x, _hand_gesture

    _lock.acquire()
    _hand_pos_x = data.x
    _hand_pos_y = data.y
    _hand_gesture = data.gesture
    _pointer_x = data.pointer_x
    _pointer_y = data.pointer_y
    _lock.release()


def init(dimensions: tuple[int, int]) -> None:
    """
    This function must be called exactly once before any input will be read
    """
    _wrapper = GestureWrapper(dimensions)
    stream = _wrapper.create_stream(_process_data)
    thread = threading.Thread(target=stream.begin_read, daemon=True)
    thread.start()


def close() -> None:
    if _wrapper is not None:
        _wrapper.close()
