var  passwordstrength = function(s){
  var i =0;
  var check1 = false, check2 =false;
  var check3 = false;
  for(i=0;i<s.length;i++)
  {
    if(s.charAt(i)>='a'&&s.charAt(i)<='z')
    check1=true;
    else if(s.charAt(i)>='A'&&s.charAt(i)<='Z')
    check2 = true;
    else if(s.charAt(i)>='0'&&s.charAt(i)<='9')
    check3= true;
  }
   if(check1&&check2&&check2)
   return true;
   else
   return false;
};

var check_length = function(username){
   if(username.length>7)
   return true;
   else
   return false;
};

function messages()
{
    $(ajax).({
    url:'/return_message',
    type:'POST',
    data:{
    reciever:reciever
    }
    })
}