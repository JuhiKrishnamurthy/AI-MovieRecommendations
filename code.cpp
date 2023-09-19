#include<iostream>
using namespace std;
class strings{
private:
	string str1;
	string res_string
public:
	strings()
	{
		str1="";
	}
	strings(string s1)
	{
		str1=s1;
	}
	string get_string()
	{
		return str1;
	}
	string operator +(strings x)
    {
    	res_string = strcat(s1, x.s1);
        return res_string; 
    }
    string operator >(strings x)
	{
		if(int(str1[0])<int(x.str1[0]))
			return 1;
		else
			return 0;
	}

};
int main()
{
	string str1,str2;
	strings res_string;
	cin>>str1;
	cin>>str2;
	strings S1(str1);
	strings S2(str2);
	if(S1<S2==1)
		res_string=S1+S2;
	else
		res_string=S2+S1;
	str final_string=res_string.get_string();
	cout<<final_string;
	return 0;
}