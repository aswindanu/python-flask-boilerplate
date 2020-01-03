import json
from . import app, client, cache, create_token, create_token_noninternal


class TestbookCrud():

    book_id1 = 0
    
    book_id2 = 0


########### PUBLIC 
########## GET
    def test_get_public_book_list_valid(self, client):
        res = client.get('pets')

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_public_book_list_invalid(self, client):
        res = client.get('pets')

        res_json = json.loads(res.data)
        assert res.status_code == 404



################################
############### PETS ###########
################################
############### POST

    def test_post_penerbit_book_invalid(self, client):
        token = create_token_noninternal()
        data = {
            "writer":"sutoyo"
        }
        res = client.post('/penerbit/buku', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_penerbit_book_valid(self, client):
        token = create_token_noninternal()
        data = {
            "title":"test1",
            "isbn":"11",
            "penerbit":"test1",
            "client_id":2
        }

        res = client.post('/penerbit/buku', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestbookCrud.book_id1 = res_json['id']
    
        assert res.status_code == 200


############## GET
    def test_get_penerbit_book_valid(self, client):
        token = create_token_noninternal()
        res = client.get('penerbit/buku',headers={'Authorization':'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200

    def test_get_penerbit_book_invalid(self, client):
        # token = create_token_noninternal()
        res = client.get('penerbit/buku/',headers={'Authorization':'Bearer 2323'})

        res_json = json.loads(res.data)
        assert res.status_code == 404


##############################
##############INTERNAL########
##############################



    def test_get_book_list_invalid(self, client):
        res = client.get('/internal/buku', 
                        headers={'Authorization': 'Bearer asasd' })

        res_json = json.loads(res.data)
        assert res.status_code == 500

    def test_get_book_list_valid(self, client):
        token = create_token()
        res = client.get('/internal/buku', 
                        headers={'Authorization': 'Bearer ' + token})

        res_json = json.loads(res.data)
        assert res.status_code == 200


############### POST

    def test_post_internal_book_invalid(self, client):
        token = create_token()
        data = {
            "writer":"sutoyo"
        }
        res = client.post('/internal/buku', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        assert res.status_code == 400

    def test_post_internal_book_valid(self, client):
        token = create_token()
       
        data = {
            "title":"test2",
            "isbn":"6",
            "penerbit":"test2",
            "client_id":2
        }

        res = client.post('/internal/buku', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )

        res_json = json.loads(res.data)
        TestbookCrud.book_id2 = res_json['id']
        assert res_json['id'] > 0
    
        assert res.status_code == 200


############### GET by id
    def test_get_by_id_internal_book_valid(self, client):
        token = create_token()
       
        res = client.get('/internal/buku/1', headers={'Authorization':'Bearer ' + token})
    
        assert res.status_code == 200


    def test_get_by_id_internal_book_invalid(self, client):
        token = create_token()
       

        res = client.get('/internal/buku/0', headers={'Authorization':'Bearer ' + token})
        
    
        assert res.status_code == 404


########### PUT

    def test_put_internal_book_valid(self, client):
        token = create_token()
       
        data = {
            "title":"test_put",
            "isbn":"10",
            "penerbit":"test_put",
            "client_id":2
        }

        res = client.put('/internal/buku/1', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 200


    def test_put_internal_book_invalid(self, client):
        token = create_token()
       
        data = {
            "penerbit":"test2"
        }

        res = client.put('/internal/buku/1', headers={'Authorization':'Bearer ' + token}, data=json.dumps(data),
                                    content_type='application/json'
        )
    
        assert res.status_code == 400

########### delete

    def test_delete_internal_book_valid1(self, client):
        token = create_token()

        res = client.delete(f'/internal/buku/{TestbookCrud.book_id1}', headers={'Authorization':'Bearer ' + token})
        assert res.status_code == 200
    
    def test_delete_internal_book_valid2(self, client):
        token = create_token()

        res = client.delete(f'/internal/buku/{TestbookCrud.book_id2}', headers={'Authorization':'Bearer ' + token})
        assert res.status_code == 200

    def test_delete_book_invalid(self, client):
        token = create_token()

        res = client.delete('/internal/buku/0', headers={'Authorization':'Bearer ' + token},
                                    content_type='application/json'
        )
        assert res.status_code == 404



