

//棋子半径为15px
weiQiController.r = 14;
weiQiController.lineThick =15;
weiQiController.blackPointR = 5;

//棋盘参数 单位为px
weiQiController.chessBoardParm = {
    'rectOrigin':[350,10],
    'width'  : 605,
    'height' : 600,
    'margin' : 30
};


$(document).ready(function(){
    weiQiController.board = $('#chessboard')[0].getContext("2d");
    weiQiController.drawBoard(); //棋盘画板
    weiQiController.getChessPosition(weiQiController.dyadic_array);
    setInterval(weiQiController.getRealtimeChessPosition,5000);
});


//画线
weiQiController.drawLine = function(ctx,x1,y1,x2,y2){
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    weiQiController.board.stroke();
}

//画黑点
weiQiController.drawBlackpoint = function(ctx,x,y,r){
    var grd=ctx;
    grd.beginPath();
    grd.arc(x,y,r,0,Math.PI*2,false);
    grd.fillStyle='#050505';
    grd.fill();
}

//画黑子
weiQiController.drawBlackChess = function(ctx,x,y,r){
    var grd=ctx.createLinearGradient(x-r,y,x+r,y);
    grd.addColorStop(0,"#050505");
    grd.addColorStop(1,"#515151");
    ctx.beginPath();
    ctx.fillStyle=grd;
    ctx.arc(x,y,r,0,2*Math.PI);
    ctx.fill();
}


//画白子
weiQiController.drawWhiteChess = function(ctx,x,y,r){
    var grd=ctx.createLinearGradient(x-r,y,x+r,y);
    grd.addColorStop(0,"#FFFACD");
    grd.addColorStop(1,"#ADADAD");
    ctx.beginPath();
    ctx.fillStyle=grd;
    ctx.arc(x,y,r,0,2*Math.PI);
    ctx.fill();
}


//画棋盘
weiQiController.drawBoard = function(){
    weiQiController.board.fillStyle="#CC9933";
    weiQiController.board.fillRect(weiQiController.chessBoardParm['rectOrigin'][0],
    weiQiController.chessBoardParm['rectOrigin'][1],
    weiQiController.chessBoardParm['width'],weiQiController.chessBoardParm['height']);     //parm : 起始坐标、宽高

    for(var i=1;i<20;i++){
        //画横线
        weiQiController.drawLine(weiQiController.board,
        weiQiController.chessBoardParm['rectOrigin'][0]+weiQiController.chessBoardParm['margin'],
        2*weiQiController.lineThick*i+weiQiController.chessBoardParm['rectOrigin'][1],
        weiQiController.chessBoardParm['rectOrigin'][0]+19*2*weiQiController.lineThick,
        2*weiQiController.lineThick*i+weiQiController.chessBoardParm['rectOrigin'][1]);
        //画竖线
        weiQiController.drawLine(weiQiController.board,
        weiQiController.chessBoardParm['rectOrigin'][0]+2*weiQiController.lineThick*i,
        2*weiQiController.lineThick+weiQiController.chessBoardParm['rectOrigin'][1],
        weiQiController.chessBoardParm['rectOrigin'][0]+2*weiQiController.lineThick*i,
        19*2*weiQiController.lineThick+weiQiController.chessBoardParm['rectOrigin'][1]);
    }
    for(var j=0;j<3;j++){
        for(var k=0;k<3;k++){
            weiQiController.drawBlackpoint(weiQiController.board,
            weiQiController.chessBoardParm['rectOrigin'][0]+2*weiQiController.lineThick*(4+j*6),
            2*weiQiController.lineThick*(4+k*6)+weiQiController.chessBoardParm['rectOrigin'][1],
            weiQiController.blackPointR
        );
        }
    }
}


//获取棋子位置  1为黑子  2为白子  0为空白
weiQiController.getChessPosition = function(positionArray){
    for(var y=0;y<positionArray.length;y++){
        for(var x=0;x<positionArray[y].length;x++){
            if(positionArray[y][x] == 1 ){
                weiQiController.drawBlackChess(weiQiController.board,
                weiQiController.chessBoardParm['rectOrigin'][0]+2*weiQiController.lineThick*(x+1),
                2*weiQiController.lineThick*(y+1)+weiQiController.chessBoardParm['rectOrigin'][1]
                ,weiQiController.r);
            }

            if(positionArray[y][x] == 2){
                weiQiController.drawWhiteChess(weiQiController.board,
                weiQiController.chessBoardParm['rectOrigin'][0]+2*weiQiController.lineThick*(x+1),
                2*weiQiController.lineThick*(y+1)+weiQiController.chessBoardParm['rectOrigin'][1]
                ,weiQiController.r);
            }
        }
    }
}

//ajax 请求最新棋局矩阵
weiQiController.getRealtimeChessPosition = function(){
    $.ajax({
        type : "get",
        url : "/relay/",
        async : false,
        success : function(data){
            //console.log(data);
            weiQiController.drawBoard();
            weiQiController.getChessPosition(data);
        }
    });
}


