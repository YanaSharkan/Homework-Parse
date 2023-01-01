from urllib import parse as parse_url
from http.cookies import SimpleCookie


def parse(query: str) -> dict:
    splitted_url = parse_url.urlsplit(query)
    return dict(parse_url.parse_qsl(splitted_url.query))


if __name__ == '__main__':
    assert parse(
        'https://example.com/path/to/page?name=ferret&color=purple'
    ) == {'name': 'ferret', 'color': 'purple'}
    assert parse(
        'https://example.com/path/to/page?name=ferret&color=purple&'
    ) == {'name': 'ferret', 'color': 'purple'}
    assert parse('http://example.com/') == {}
    assert parse('http://example.com/?') == {}
    assert parse('http://example.com/?name=Dima') == {'name': 'Dima'}
    assert parse('http://example.com/?testparam=&testparam1=value') == \
           {'testparam1': 'value'}
    assert parse('http://example.com/?testparam=%26') == \
           {'testparam': '&'}
    assert parse('http://example.com/?testparam=test%3f&param1=value') == \
           {'testparam': 'test?', 'param1': 'value'}
    assert parse('http://test.com?testparam=value#hashparam=value1') == \
           {'testparam': 'value'}
    assert parse('http://example.com/?test') == {}


def parse_cookie(query: str) -> dict:
    cookie = SimpleCookie()
    cookie.load(query)
    return {k: v.value for k, v in cookie.items()}


if __name__ == '__main__':
    assert parse_cookie('name=Dima;') == \
           {'name': 'Dima'}
    assert parse_cookie('') == {}
    assert parse_cookie('name=Dima;age=28;') == \
           {'name': 'Dima', 'age': '28'}
    assert parse_cookie('name=Dima=User;age=28;') == \
           {'name': 'Dima=User', 'age': '28'}
    assert parse_cookie('test') == {}
    assert parse_cookie('test=') == \
           {'test': ''}
    assert parse_cookie(';test=') == {}
    assert parse_cookie('=test') == {}
    assert parse_cookie('T=\"test\"') == \
           {'T': 'test'}
    assert parse_cookie('\"T\"=test') == {}
    assert parse_cookie('test=test;;param=value') == \
           {'test': 'test'}
    assert parse_cookie('test=";"') == {'test': ';'}
    assert parse_cookie('test="param";test="param_2"') == \
           {'test': 'param_2'}
