LoadPackage("GAPic");
Read("FindOuterTriangle.g");

rot90:=[[0,1,0],[-1,0,0],[0,0,1]];;

coordinates_middle:=[[0,0,0],[2,0,0],[2,-2,0],[0,-2,0]];;

coordinates_up:=[
			[1,1,1],[2,0,1],[1,-1,1],[0,-2,1],[-1,-1,1],[0,0,1]
];;

coordinates:=Concatenation(coordinates_middle,coordinates_up);;

coordinates:=coordinates*    DiagonalMat([1,1,Sqrt(2.)])-[0,-2,0];;

coordinates:=coordinates*rot90;

#middle connected to upper part
vof_block:=[
[1,2,3],[1,3,4],

[5,6,7],[7,8,9],[5,7,10],[7,10,9],

[1,10,5],[1,10,9],[5,1,2],[5,6,2],[6,2,7],[7,2,3],[7,3,4],[4,8,7],[4,8,9],[4,9,1]

];;

s:=SimplicialSurfaceByVerticesInFaces(vof_block);;
pr:=SetVertexCoordinates3D(s,coordinates);;



x:=5;
y:=5;

a:=0.01;

vof_assembly:=[];
coordinates_assembly:=[];

# create the incidence structure and coordinates
for i in [1..x] do
	for j in [1..y] do
		if i = 1 then
			vof_assembly:=Concatenation(vof_assembly,vof_block+(y*(i-1)+(j-1))*1*NumberOfVertices(s));
			
			if i mod 2 = 0 then
				coordinates_assembly:=Concatenation(coordinates_assembly,brcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
			else
				coordinates_assembly:=Concatenation(coordinates_assembly,trcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
			fi;
			
			Print("i = ",i, " j = ",j,"\n");
			Print("offset ",(y*(i-1)+(j-1)),"\n");
		fi;
		if not i = 1 and not i = x then
			if j = 1 then
				vof_assembly:=Concatenation(vof_assembly,vof_block+((y-1)+2*(i-1)+(j-1)-1)*1*NumberOfVertices(s));

				if i mod 2 = 0 then
					coordinates_assembly:=Concatenation(coordinates_assembly,brcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
				else
					coordinates_assembly:=Concatenation(coordinates_assembly,trcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
				fi;

				Print("i = ",i, " j = ",j, "\n");
				Print("offset ",((y-1)+2*(i-1)+(j-1)-1),"\n");
			fi;
			if j = y then
				vof_assembly:=Concatenation(vof_assembly,vof_block+((y-1)+2*(i-1)+(1)-1)*1*NumberOfVertices(s));

				if i mod 2 = 0 then
					coordinates_assembly:=Concatenation(coordinates_assembly,brcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
				else
					coordinates_assembly:=Concatenation(coordinates_assembly,trcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
				fi;

				Print("i = ",i, " j = ",j, "\n");
				Print("offset ",((y-1)+2*(i-1)+(1)-1),"\n");
			fi;
		fi;
		if i = x then
			vof_assembly:=Concatenation(vof_assembly,vof_block+(y+(x-2)*2+j-1)*1*NumberOfVertices(s));

			if i mod 2 = 0 then
				coordinates_assembly:=Concatenation(coordinates_assembly,brcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
			else
				coordinates_assembly:=Concatenation(coordinates_assembly,trcoords+[2+a,0,0]*(i-1)+[0,2+a,0]*(j-1));
			fi;

			Print("i = ",i, " j = ",j,"\n");
			Print("offset ",((y-1)+(x-2)*2+j),"\n");
		fi;
	od;
od;


# combine to stl file


pr_assembly:=rec();
s_assembly:=SimplicialSurfaceByVerticesInFaces(vof_assembly);;

#data:=JoinComponents(s_assembly,coordinates_assembly*1.,0.0001);
#ComponentsOuterHull([data[2],data[1]], "frame-1", 0.0001, false);

ComponentsOuterHull([s_assembly, coordinates_assembly*1.0], "frame-3", 0.0001, false);
#ComponentsOuterHull([s, coordinates*1.0], "frame-1a", 0.0001, false);

#verticesPositions:=coordinates_assembly;
#printRecord := SetVertexCoordinates3D(s_assembly, verticesPositions, rec());
#params := [["a", 0, [-1,10]]];
#printRecord := SetVertexParameters(s_assembly, params, printRecord);

#printRecord := ActivateInnerCircles(s_assembly, printRecord);

#DrawComplexToJavaScript(s_assembly, "frame-1a.html", printRecord);


