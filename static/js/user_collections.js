function add_collections(username){
    let u = document.URL;
    if (u.endsWith('/') === false) {
        u = u+'/';
    }
    let a = u.split('/');
    let book_id = a[a.length-3];
    let chapter_count = a[a.length-2];

    $.post('http://127.0.0.1/api/user_collections',
        {'u': username, 'book_id': book_id, 'chapter_count': chapter_count},
        function(data,status,xhr){
        alert(data['msg']);
        // console.log(status, data);
        },
        'json' )
}

function delete_collections(user, book_id, chapter_count){

    let url = `http://127.0.0.1/api/${book_id}/${chapter_count}`;
    // console.log(url);
    $.ajax({url:url,
        data:{'u': user, 'book_id': (book_id), 'chapter_count': chapter_count},
        success:function(result){alert(result['msg']);location.reload();},
        type:'delete',
        dataType: 'json'
    })
}