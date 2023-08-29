LoadPackage("GAPic");
Read("FindOuterTriangle.g");

rot90:=[[0,1,0],[-1,0,0],[0,0,1]];;

flipx:=[[-1,0,0],[0,1,0],[0,0,1]];;

flipy:=[[1,0,0],[0,-1,0],[0,0,1]];;


coordinates_middle:=[[0,0,0],[2,0,0],[2,-2,0],[0,-2,0]];;

coordinates_up:=[
			[1,1,1],[2,0,1],[1,-1,1],[0,-2,1],[-1,-1,1],[0,0,1]
];;

coordinates:=Concatenation(coordinates_middle,coordinates_up);;

coordinates:=coordinates*    DiagonalMat([1,1,Sqrt(2.)])-[0,-2,0];;

#coordinates:=coordinates+2;

#coordinates:=coordinates*rot90;

# create the orientations of the block and move it to the origin as one of the corners
brcoords:=coordinates;
trcoords:=coordinates*rot90+[2,0,0];
tlcoords:=coordinates*rot90^2+[2,0,0]+[0,2,0];
blcoords:=coordinates*rot90^3+[0,2,0];


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
for i in [2..x-1] do
	for j in [2..y-1] do
		vof_assembly:=Concatenation(vof_assembly,vof_block+((y-2)*(i-2)+(j-2))*1*NumberOfVertices(s));
		
		if i mod 2 = 0 then
			if j mod 2 = 0 then
				coordinates_assembly:=Concatenation(coordinates_assembly,brcoords+[2+a,0,0]*(i)+[0,2+a,0]*(j));
			else
				coordinates_assembly:=Concatenation(coordinates_assembly,blcoords+[2+a,0,0]*(i)+[0,2+a,0]*(j));
			fi;
		else
			if j mod 2 = 0 then
				coordinates_assembly:=Concatenation(coordinates_assembly,trcoords+[2+a,0,0]*(i)+[0,2+a,0]*(j));
			else
				coordinates_assembly:=Concatenation(coordinates_assembly,tlcoords+[2+a,0,0]*(i)+[0,2+a,0]*(j));
			fi;
		fi;
		#coordinates_assembly:=Concatenation(coordinates_assembly,(coordinates*rot90^(i mod 2)+[0+a,0,0]*(i-1)+[0,0+a,0]*(j-1)));
	od;
od;


# combine to stl file


pr_assembly:=rec();
s_assembly:=SimplicialSurfaceByVerticesInFaces(vof_assembly);;

#data:=JoinComponents(s_assembly,coordinates_assembly*1.,0.0001);
#ComponentsOuterHull([data[2],data[1]], "frame-1", 0.0001, false);

ComponentsOuterHull([s_assembly, coordinates_assembly*1.0], "interlocking-2", 0.0001, false);
#ComponentsOuterHull([s, coordinates*1.0], "interlocking-1a", 0.0001, false);

#verticesPositions:=coordinates_assembly;
#printRecord := SetVertexCoordinates3D(s_assembly, verticesPositions, rec());
#params := [["a", 0, [-1,10]]];
#printRecord := SetVertexParameters(s_assembly, params, printRecord);

#printRecord := ActivateInnerCircles(s_assembly, printRecord);

#DrawComplexToJavaScript(s_assembly, "frame-1a.html", printRecord);


