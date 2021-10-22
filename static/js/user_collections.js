function add_collections(username){
    if (!username){alert('未登陆');return false;}
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
        'json' );
    return true;
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

function add_comment(book_id, chapter_count){
    let user = $('input#input_comment_user_name').val()
    let comment = $('textarea#input_comment').val();
    let url = `http://127.0.0.1/api/comment/${book_id}/${chapter_count}`;
    // console.log(user, book_id, chapter_count, comment);
    $.ajax({
        url:url,
        data: {'u': user, 'comment': comment},
        success: function(result){if (check_result(result)){alert('提交评论成功')}else{alert(result['msg']);}location.reload();},
        type: 'post',
        dataType: 'json'
    })
}

function check_result(result){
    return result['result']
}