import requests

def match(pred, target):
    for item in pred:
        if item not in target:
            return False
    return True

def test_spell_check():
    word = "গ্রাহমদেব"
    response = requests.post("http://localhost:8080/check", json={"word": word})
    print(response.json())
    assert response.status_code == 200
    assert match(list(response.json()), ["গ্রাহকদের","গ্রাহদের","গ্রামদেশ"]) == True


if __name__ == "__main__":
    test_spell_check()