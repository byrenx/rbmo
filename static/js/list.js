List.prototype.list = [];
List.prototype.add = function(item){
    this.list.push(item);
}

List.prototype.del = function(item){
   var temp = [];
   while(this.list.length>0){
       item_popped = this.list.pop();
       if(item_popped!=item){
	   temp.push(item_popped);
       }
   }
   this.list=temp; 
}

List.prototype.found = function(item){
    var found = false;
    for(var i=0; i<this.list.length; i++){
	if(this.list[i]==item){
	    found=true;
	    break;
	}
    }
    return found;
}

function List(){
    this.list = [];
}

