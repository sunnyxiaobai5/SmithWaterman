#include <stdio.h>
#include <stdlib.h>
#define MAXLEN  1000    //序列最大长度
#define L1 31	//序列1长度
#define L2 30	//序列2长度
#define MROW (L2+1)	//分值矩阵行数
#define MCOL (L1+1)	//分值矩阵列数
#define NO 0    //不设置指针
#define UP 1    //由上方得到值
#define LEFT 2  //由左方得到值
#define LU  3   //由左上方得到值

int dir=NO ;    //存储当前格子指针应该指向的方向


//输出初始序列
void init_seq(int *Ps1,int *Ps2,int l1,int l2)
{
	int i,j;
 	//打印序列1
	printf("原序列1：");
	for(i=0;i<l1;i++)
	for(i=0;i<l1;i++)
		printf("%c ",Ps1[i]);
	printf("\n");

	//打印序列2
	printf("原序列2：");
	for(i=0;i<l2;i++)
		printf("%c ",Ps2[i]);
	printf("\n");

}

//辅助函数，输出矩阵信息
void output(int *Ps1,int *Ps2,int l1,int l2,int matrix[MROW][MCOL],int Pm[MROW][MCOL])
{
    int i,j;
 
    //输出带序列的分值矩阵
    printf("     ");
	for(i=0;i<l1;i++)
		printf("%4c",Ps1[i]);
	printf("\n");

	for(i=0;i<MROW;i++)
	{
        if(i==0 || i==MROW)
            printf(" ");

		if(i>0)
            printf("%-4c",Ps2[i-1]);
		for(j=0;j<MCOL;j++)
		{
		    if(i==0 || i==MROW)
                printf("%4d",matrix[i][j]);
		    else
				printf("%-4d",matrix[i][j]);
		}
		printf("\n");
	}
	for(i=0;i<MROW;i++)
	{
	    printf(" ");
	    for(j=0;j<MCOL;j++)
	        printf("%4d",Pm[i][j]);
	    printf("\n");
	}
	printf("\n");
}

//获取当前格子应该设置的值
int get_max(int r[MROW][MCOL],int s1[],int s2[],int i,int j,int *dir)
{
	int gap=-1;
	if(s1[j-1]==s2[i-1])
		gap=1;
    //初始时将最大值设置为左上格子，并将方向设置为左上
    int temp=r[i-1][j-1] + gap;
    *dir=LU;
    //若左上角得到的值小于上方得到的值，设置最大值为上方，并将方向设为向上
    if(temp<r[i-1][j]-1)
    {
        temp=r[i-1][j]-1;
        *dir=UP;
    }
    //若左上角和上方中最大值小于左边格子值，设置最大值为左方值，并将方向设为向左
    if(temp<r[i][j-1]-1)
    {
        temp=r[i][j-1]-1;
        *dir=LEFT;
    }
    //根据获取的最大值得到当前值，若当前值小于0，将当前值设置为且不设置方向指针
    if(temp<=0)
    {
        *dir=NO;
        temp=0;
    }
	return temp;
}

//构造分值矩阵和方向矩阵
void create_matrix(int row,int col,int m[MROW][MCOL],int Pm[MROW][MCOL],int *s1,int *s2)
{
	int i,j;
	for(i=1;i<row;i++)
	{
		for(j=1;j<col;j++)
		{
		    int dir=NO;
			if(s1[j-1]==s2[i-1])
			{
			    //相等，设置其值为左上角格子值+1,设置指针指向左上角
				m[i][j]=m[i-1][j-1]+1;
				Pm[i][j]=LU;
			}
			else{
			    //不等，获取当前格子的值，并设置其方向
                int cur=get_max(m,s1,s2,i,j,&dir);
                m[i][j]=cur;
                Pm[i][j]=dir;
			}
		}
	}
}

//输出最终形成的两个序列
void result(int m[MROW][MCOL],int Pm[MROW][MCOL],int *Ps1,int *Ps2)
{
	int i,j;
    int max=0;
    int m_row=0;
    int m_col=0;
    for(i=MROW-1;i>=0;i--)
    {
        for(j=MCOL-1;j>=0;j--)
        {
            if(max<m[i][j])
            {
                max=m[i][j];
                m_row=i;
                m_col=j;
            }
        }
    }
    int cur_row=m_row;
    int cur_col=m_col;
    printf("Sequence1 ");
    while(Pm[cur_row][cur_col]!=NO)
    {
        switch(Pm[cur_row][cur_col])
        {
            case UP:
        		printf("_");
				cur_row--;
				break;
            case LEFT:
    			printf("%c",Ps1[cur_col-1]);
				cur_col--;
				break;
            case LU:
    			printf("%c",Ps1[cur_col-1]);
				cur_row--;
				cur_col--;
				break;
        }
    }
    cur_row=m_row;
    cur_col=m_col;
    printf("\nSequence2 ");
    while(Pm[cur_row][cur_col]!=NO)
    {
        switch(Pm[cur_row][cur_col])
        {
            case UP:
    		printf("%c",Ps2[cur_row-1]);
				cur_row--;
				break;
            case LEFT:
				printf("_");
				cur_col--;
				break;
            case LU:
    			printf("%c",Ps2[cur_row-1]);
				cur_row--;
				cur_col--;
				break;
        }
    }
	printf("\n");

}

int main()
{
	//初始化序列1和序列2
	int Ps1[L1]={'A','T','C','G','G','A','G','C','T','G','G','A','C','C','T','G','A','T','G','A','T','T','C','G','C','G','C','C','G','A','T'};
	int Ps2[L2]={'A','T','C','T','G','A','G','C','T','G','A','C','C','T','C','A','T','G','A','T','T','G','G','C','G','C','C','G','A','T'};
	//输出初始序列
	init_seq(Ps1,Ps2,L1,L2);
	//初始化分值矩阵
	int matrix[MROW][MCOL]={0};
	//初始化方向矩阵
	int Pm[MROW][MCOL]={NO};
	//生成分值矩阵
	create_matrix(MROW,MCOL,matrix,Pm,Ps1,Ps2);
	//输出数列与矩阵等信息
	//output(Ps1,Ps2,L1,L2,matrix,Pm);
	//输出最终的序列 注：方向相反
	result(matrix,Pm,Ps1,Ps2);
	return 0;
}
